import csv
import json
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import Any, List

from src.access.constructs import SurveyData, SurveyDataColumn
from src.access.dao import SurveyDataDao
from src.process.constructs import (
    CARCASS_AGE_RANGE_MAP,
    SURVEY_DATA_POTENTIAL_KEYS_MAP,
    SURVEY_DATA_POTENTIAL_VALUES_MAP,
    DataForYear,
)


class SurveyDataProcessor:
    def __init__(self, survey_data_dao: SurveyDataDao):
        self.survey_data_entry_processor = SurveyDataEntryProcessor()
        self.dao = survey_data_dao
        self.survey_dates_map = {}

    def process_path(self, path):
        path = Path(path)
        if not path.is_dir():
            raise ValueError(f"process_path expects a directory path, got {path}")

        dates_files = sorted(path.glob("*dates*.json"))
        data_files = sorted(
            list(path.glob("*survey*.json")) + list(path.glob("*salmon*.csv"))
        )

        self.process_survey_dates(dates_files)
        self.process_survey_data(data_files)

    def process_all_data(self, snapshot_root_path, years=[]):
        years_to_files = {}
        remaining = set([str(y) for y in years])
        process_all = not years
        snapshots_root = Path(snapshot_root_path)
        snapshot_dirs = sorted(
            [p for p in snapshots_root.iterdir() if p.is_dir()],
            key=lambda p: p.name,
            reverse=True,
        )
        print(f"Searching snapshots under {snapshots_root} for years {years}...")
        for snapshot in snapshot_dirs:
            if not process_all and not remaining:
                break
            print(f"  Searching {snapshot}...")

            snapshot_map = {}
            for file in list(snapshot.glob("*.json")) + list(snapshot.glob("*.csv")):
                prefix = file.name.split("_")[0]
                if (
                    prefix in remaining or process_all
                ) and prefix not in years_to_files.keys():
                    if prefix not in snapshot_map:
                        snapshot_map[prefix] = DataForYear(
                            year=prefix, snapshot=snapshot.name
                        )
                    if "dates" in file.name:
                        snapshot_map[prefix].dates_files.append(file)
                    else:
                        snapshot_map[prefix].data_files.append(file)
            print("  Assigning paths:")
            pprint(snapshot_map, indent=2)
            years_to_files |= snapshot_map
            remaining -= set(snapshot_map.keys())

        dates_files = [file for d in years_to_files.values() for file in d.dates_files]
        data_files = [file for d in years_to_files.values() for file in d.data_files]
        self.process_survey_dates(dates_files)
        self.process_survey_data(data_files)

    def process_survey_data(self, file_list: list):
        for file in file_list:
            try:
                print(f"Processing {file}...")
                file_path = Path(file)
                survey_data: List[SurveyData] = []
                if file_path.suffix == ".json":
                    payload = json.loads(file_path.read_text(encoding="utf-8"))
                    survey_data = [
                        self.survey_data_entry_processor.process_entry_blob(blob)
                        for blob in payload
                    ]
                elif file_path.suffix == ".csv":
                    with open(
                        file_path, mode="r", newline="", encoding="utf-8"
                    ) as csv_file:
                        reader = csv.DictReader(csv_file)
                        survey_data = [
                            self.survey_data_entry_processor.process_entry_blob(row)
                            for row in reader
                        ]
                else:
                    raise RuntimeError(f"Unsupported data file type at {file_path}")
                print(f"    generated {len(survey_data)} entries")
                for entry in survey_data:
                    self.dao.upsert(entry)
                print(f"    inserted {len(survey_data)} rows")
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")

    def process_survey_dates(self, file_list: list):
        for file in file_list:
            try:
                print(f"Processing {file}...")
                json_path = Path(file)
                payload = json.loads(json_path.read_text(encoding="utf-8"))
                for blob in payload:
                    id = blob.get("ec5_uuid")
                    date = datetime.strptime(
                        blob.get("Survey_Date", ""), "%m/%d/%Y"
                    ).strftime("%Y-%m-%d")
                    if id and date:
                        self.survey_dates_map[id] = date
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
        self.survey_data_entry_processor.survey_dates_map = self.survey_dates_map
        print(f"Dates processed: {self.survey_dates_map}")


class SurveyDataEntryProcessor:
    def __init__(self):
        self._build_normalization_maps()
        self.survey_dates_map = {}

    def process_entry_blob(self, blob: dict) -> SurveyData:
        data: dict[str, Any] = {}
        for key, value in blob.items():
            normalized_key = self.key_normalization_map.get(key)
            if normalized_key is None:
                normalized_key = self.key_normalization_map.get(
                    self._normalize_key_name(key)
                )

            if normalized_key is SurveyDataColumn.EXTERNAL_ID:
                if not data.get(SurveyDataColumn.EXTERNAL_ID.value):
                    data[SurveyDataColumn.EXTERNAL_ID.value] = str(value)
            elif normalized_key is SurveyDataColumn.SURVEY_DATE:
                data[SurveyDataColumn.SURVEY_DATE.value] = self._parse_date(value)
            elif normalized_key is SurveyDataColumn.DISTANCE:
                data[SurveyDataColumn.DISTANCE.value] = self._parse_int(value)
            elif normalized_key is SurveyDataColumn.QUANTITY:
                data[SurveyDataColumn.QUANTITY.value] = self._parse_int(value)
            elif normalized_key is SurveyDataColumn.LENGTH:
                data[SurveyDataColumn.LENGTH.value] = self._parse_float(value)
            elif normalized_key is SurveyDataColumn.WIDTH:
                data[SurveyDataColumn.WIDTH.value] = self._parse_float(value)
            elif normalized_key is SurveyDataColumn.CARCASS_AGE_LABEL:
                label, min_age, max_age = self._parse_carcass_age(value)
                data[SurveyDataColumn.CARCASS_AGE_LABEL.value] = label
                data[SurveyDataColumn.CARCASS_AGE_MIN.value] = min_age
                data[SurveyDataColumn.CARCASS_AGE_MAX.value] = max_age
            elif key in {"Location", "location"}:
                data.update(self._parse_location(value))
            elif normalized_key:
                data[normalized_key.value] = self._normalize_value(
                    normalized_key, value
                )

        # default quantity to 1
        if SurveyDataColumn.QUANTITY.value not in data:
            data[SurveyDataColumn.QUANTITY.value] = 1
        # fetch survey date from map for epicollect data
        if SurveyDataColumn.SURVEY_DATE.value not in data:
            date_key = blob.get("ec5_parent_uuid")
            date = self.survey_dates_map.get(date_key)
            data[SurveyDataColumn.SURVEY_DATE.value] = self._parse_date(date)
        if data.get(SurveyDataColumn.SURVEY_DATE.value):
            data[SurveyDataColumn.YEAR] = data.get(
                SurveyDataColumn.SURVEY_DATE.value
            ).year

        return SurveyData(**data)

    def _parse_date(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return None
            try:
                return datetime.fromisoformat(text.replace("Z", "+00:00"))
            except ValueError:
                try:
                    return datetime.strptime(text, "%Y-%m-%d")
                except ValueError:
                    return None
        return None

    def _parse_int(self, value):
        if value is None:
            return None
        try:
            return int(float(str(value).strip()))
        except (ValueError, TypeError):
            return None

    def _parse_float(self, value):
        if value is None:
            return None
        try:
            return float(str(value).strip())
        except (ValueError, TypeError):
            return None

    def _is_int(self, value):
        if value is None:
            return False
        try:
            number = float(str(value).strip())
        except (ValueError, TypeError):
            return False
        return number.is_integer()

    def _normalize_string(self, value):
        if value is None:
            return None
        text = str(value).strip().replace("_", " ")
        return text or None

    def _normalize_value(self, normalized_key, value):
        if not value:
            return None
        lookup = self.data_normalization_map.get(normalized_key, {})
        normalized_value = lookup.get(str(value).strip().lower())
        return normalized_value if normalized_value is not None else value

    def _normalize_key_name(self, key):
        if not isinstance(key, str):
            return key
        return key.strip().lower().replace(" ", "_")

    def _parse_carcass_age(self, value):
        if self._is_int(value):
            hours = int(float(str(value).strip()))
            return value, hours, hours
        else:
            normalized_label = self._normalize_value(
                SurveyDataColumn.CARCASS_AGE_LABEL, value
            )
            min_age, max_age = CARCASS_AGE_RANGE_MAP.get(normalized_label, (None, None))
            return normalized_label, min_age, max_age

    def _parse_location(self, location_blob):
        if isinstance(location_blob, str):
            parts = location_blob.strip().split()
            if len(parts) >= 2:
                lat = self._parse_float(parts[0])
                lon = self._parse_float(parts[1])
                accuracy = self._parse_float(parts[-1]) if len(parts) >= 4 else None
                return {
                    SurveyDataColumn.LATITUDE.value: lat,
                    SurveyDataColumn.LONGITUDE.value: lon,
                    SurveyDataColumn.ACCURACY.value: accuracy,
                }
        elif isinstance(location_blob, dict):
            return {
                SurveyDataColumn.LATITUDE.value: self._parse_float(
                    location_blob.get("latitude")
                ),
                SurveyDataColumn.LONGITUDE.value: self._parse_float(
                    location_blob.get("longitude")
                ),
                SurveyDataColumn.ACCURACY.value: self._parse_float(
                    location_blob.get("accuracy")
                ),
            }
        return {}

    def _build_normalization_maps(self):
        self.data_normalization_map = {}
        self.key_normalization_map = {}
        for column, value_map in SURVEY_DATA_POTENTIAL_VALUES_MAP.items():
            self.data_normalization_map[column] = {}
            for n_value, p_values in value_map.items():
                all_potential_values = set(p_values)
                for p_value in p_values:
                    snake_case = "_".join(p_value.split(" "))
                    if snake_case not in all_potential_values:
                        all_potential_values.add(snake_case)
                for v in all_potential_values:
                    self.data_normalization_map[column][v] = n_value

        for key, p_keys in SURVEY_DATA_POTENTIAL_KEYS_MAP.items():
            for p_key in p_keys:
                self.key_normalization_map[p_key] = key
                if isinstance(p_key, str):
                    self.key_normalization_map[p_key.lower()] = key
                    self.key_normalization_map[self._normalize_key_name(p_key)] = key
