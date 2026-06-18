from datetime import datetime

import pytest

from src.access.constructs import Species, SurveyData
from src.validation.constructs import SurveyDataAssertion
from src.validation.validator import SurveyDataValidator


@pytest.fixture
def insert_survey_data(survey_data_dao):
    """Helper fixture for inserting rows into survey_data table."""

    def _insert(external_id, survey_date, species, quantity, year):
        survey_data_dao.upsert(
            SurveyData(
                external_id=external_id,
                survey_date=survey_date,
                species=species,
                quantity=quantity,
                year=year,
            )
        )

    return _insert


def test_get_survey_data_yearly_stats_counts_rows(survey_data_dao, insert_survey_data):
    insert_survey_data("e1", datetime(2024, 1, 1), Species.CHUM, 3, 2024)
    insert_survey_data("e2", datetime(2024, 1, 2), Species.COHO, 2, 2024)

    validator = SurveyDataValidator(survey_data_dao)
    stats = validator.get_survey_data_yearly_stats()

    assert stats[2024][SurveyDataAssertion.EXPECTED_CHUM_COUNT] == 3
    assert stats[2024][SurveyDataAssertion.EXPECTED_COHO_COUNT] == 2
    assert stats[2024][SurveyDataAssertion.ENTRY_WITH_DISTANCE] == 0


def test_validate_db_with_matching_snapshot_does_not_raise(
    survey_data_dao, insert_survey_data
):
    insert_survey_data("e1", datetime(2024, 1, 1), Species.CHUM, 1, 2024)

    validator = SurveyDataValidator(survey_data_dao)
    snapshot = validator.get_survey_data_yearly_stats()
    validator.validate_db(info_snapshot=snapshot)


def test_validate_db_with_mismatched_snapshot_raises(
    survey_data_dao, insert_survey_data
):
    insert_survey_data("e1", datetime(2024, 1, 1), Species.CHUM, 1, 2024)

    validator = SurveyDataValidator(survey_data_dao)
    snapshot = validator.get_survey_data_yearly_stats()
    bad_snapshot = {
        2024: {
            SurveyDataAssertion.EXPECTED_CHUM_COUNT: snapshot[2024][
                SurveyDataAssertion.EXPECTED_CHUM_COUNT
            ]
            + 1
        }
    }

    with pytest.raises(AssertionError):
        validator.validate_db(info_snapshot=bad_snapshot)
