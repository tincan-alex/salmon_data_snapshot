from datetime import datetime, timezone
from pprint import pprint

from src.access.constructs import SURVEY_DATA_TABLE_NAME, Species, StreamLabel, SurveyDataColumn
from src.access.dao import SurveyDataDao
from src.access.constructs import SurveyType
from src.access.query_builder import distinct_counts_query, presence_count_query, value_count_query
from src.validation.constructs import SURVEY_DATA_DISTINCT_VALUE_ASSERTIONS, SURVEY_DATA_EXPECTED_COUNTS_MAP, SURVEY_DATA_PRESENCE_ASSERTIONS, SurveyDataAssertion


class SurveyDataValidator:
    def __init__(self, survey_data_dao: SurveyDataDao):
        self.dao = survey_data_dao

    # for every past survey year
    # - expected live/dead/redd counts
    # - expected chum count
    # - expected coho count
    # sanity check for every survey year
    #   - there exist entries for all possible values of adipose fin, predation, spawn
    #   - there exist entries with notes
    #   - there exist non-0 distance counts
    #   - there exist piper creek entries
    #   - there exist lat and lon values
    # sanity checks are warnings if the current year is the latest year in db
    def validate_db(self, raise_on_failure=True):
        oldest_year, newest_year, yearly_info = self._gather_info()
        print(f"Running validation on database from {oldest_year} to {newest_year}...")

        errors, warnings = self._run_validation(oldest_year, newest_year, yearly_info)
        print("Collected yearly stats:")
        pprint(yearly_info, indent=4)
        print("Warnings:")
        pprint(warnings, indent=4)
        print("Errors:")
        pprint(errors, indent=4)

        if raise_on_failure and errors:
            raise AssertionError(f"Database validation failed with errors:\n{'\n'.join(errors)}")

    def _gather_info(self):
        years = self.dao.query(f"SELECT MIN({SurveyDataColumn.YEAR}), MAX({SurveyDataColumn.YEAR}) from {SURVEY_DATA_TABLE_NAME};")
        if not years or len(years) < 1:
            raise AssertionError(f"Missing data from survey DB: {years}")

        oldest_year, newest_year = years[0]
        yearly_info = {}
        for year in range(oldest_year, newest_year+1):
            yearly_info[year] = self._gather_info_for_year(year)
        
        return oldest_year, newest_year, yearly_info

    def _gather_info_for_year(self, year):
        return {
            SurveyDataAssertion.EXPECTED_LIVE_COUNT: self._get_count_by_value(SurveyDataColumn.SURVEY_TYPE, SurveyType.LIVE, year),
            SurveyDataAssertion.EXPECTED_DEAD_COUNT: self._get_count_by_value(SurveyDataColumn.SURVEY_TYPE, SurveyType.DEAD, year),
            SurveyDataAssertion.EXPECTED_REDD_COUNT: self._get_count_by_value(SurveyDataColumn.SURVEY_TYPE, SurveyType.REDD, year),
            SurveyDataAssertion.EXPECTED_CHUM_COUNT: self._get_count_by_value(SurveyDataColumn.SPECIES, Species.CHUM, year),
            SurveyDataAssertion.EXPECTED_COHO_COUNT: self._get_count_by_value(SurveyDataColumn.SPECIES, Species.COHO, year),
            SurveyDataAssertion.ADIPOSE_FIN_STATUSES: self._get_distinct_counts(SurveyDataColumn.ADIPOSE_FIN, year),
            SurveyDataAssertion.PREDATION_STATUSES: self._get_distinct_counts(SurveyDataColumn.PREDATION, year),
            SurveyDataAssertion.SPAWN_STATUSES: self._get_distinct_counts(SurveyDataColumn.SPAWNED, year),
            SurveyDataAssertion.ENTRY_ON_PIPERS_CREEK: self._get_count_by_value(SurveyDataColumn.STREAM, StreamLabel.PIPER.replace("'", "''"), year),
            SurveyDataAssertion.ENTRY_WITH_DISTANCE: self._get_count_by_presence(SurveyDataColumn.DISTANCE, year),
            SurveyDataAssertion.ENTRY_WITH_NOTES: self._get_count_by_presence(SurveyDataColumn.NOTE, year),
            SurveyDataAssertion.ENTRY_WITH_LOCATION: self._get_count_with_location(year),
        }
    
    def _run_validation(self, oldest_year, newest_year, yearly_info):
        errors = []
        warnings = []
        current_time = datetime.now(timezone.utc)
        if oldest_year > 2019:
            errors.append(f"Missing old data at least back to 2019; oldest year in database: {oldest_year}")
        if newest_year < 2025:
            errors.append(f"Missing new data at least up to 2025; newest year in database: {newest_year}")
        if newest_year > current_time.year:
            errors.append(f"Newest survey year in database {newest_year} larger than current year")
        if current_time.year > newest_year and current_time.month > 10:
            warnings.append(f"Potentially missing current year's survey data; newest year in database: {newest_year}")

        for year, info in yearly_info.items():
            # expected past year species/type count check
            expected_counts = SURVEY_DATA_EXPECTED_COUNTS_MAP.get(year)
            if expected_counts:
                for assertion, count in expected_counts.items():
                    if info.get(assertion) != count:
                        errors.append(f"FAILED count expectation for {year} {assertion}: expected {count}, got {info.get(assertion)}")

            # sanity checks
            for assertion in SURVEY_DATA_PRESENCE_ASSERTIONS:
                if info.get(assertion, 0) < 1:
                    message = f"FAILED presence expectation for {year} {assertion}: expected at least 1, got none"
                    if year == current_time.year:
                        warnings.append(message)
                    else:
                        errors.append(message)

            # adipose fin/predation/spawn statuses presence check
            for assertion, values in SURVEY_DATA_DISTINCT_VALUE_ASSERTIONS.items():
                for value in values:
                    if info.get(assertion, {}).get(value, 0) < 1:
                        message = f"FAILED presence expectation for {year} {assertion} {value}: expected at least 1, got none"
                        if year == current_time.year or value == "Unknown":
                            warnings.append(message)
                        else:
                            errors.append(message)
        
        return errors, warnings
            
    
    def _get_count_by_value(self, column, value, year):
        query = value_count_query(column, f"'{value}'", year)
        print(f"running query {query}")
        return self._get_count(query)
    
    def _get_count_by_presence(self, column, year):
        query = presence_count_query(column, year)
        print(f"running query {query}")
        return self._get_count(query)
    
    def _get_count_with_location(self, year):
        query = f'''
            SELECT COALESCE(SUM(CASE WHEN 
                {SurveyDataColumn.LATITUDE} IS NOT NULL
                AND abs({SurveyDataColumn.LATITUDE}) > 0.00
                AND {SurveyDataColumn.LONGITUDE} IS NOT NULL
                AND abs({SurveyDataColumn.LONGITUDE}) > 0.00
            THEN quantity END), 0) AS count FROM {SURVEY_DATA_TABLE_NAME}
            WHERE {SurveyDataColumn.YEAR} = {year}
        ;
        '''
        return self._get_count(query)

    def _get_count(self, query):
        result = self.dao.query(query)
        if not result or len(result) < 1:
            return 0
        return result[0][0]

    def _get_distinct_counts(self, column, year):
        result = self.dao.query(distinct_counts_query(column, year))
        if not result or len(result) < 1:
            return {}
        return {val: count for val, count in result}
