from datetime import datetime

import pytest

from src.access.constructs import (
    CarcassLocation,
    CarcassState,
    PredationStatus,
    Species,
    SurveyDataColumn,
)
from src.process.processor import SurveyDataEntryProcessor


@pytest.mark.parametrize(
    "blob, expected",
    [
        (
            {
                "ec5_uuid": "abc123",
                "survey_date": "2024-10-02",
                "species": "coho",
                "distance": "10",
                "quantity": "",
                "length_inches": "12.5",
                "width_inches": "3.1",
                "predation": "no damage",
            },
            {
                SurveyDataColumn.EXTERNAL_ID: "abc123",
                SurveyDataColumn.YEAR: 2024,
                SurveyDataColumn.SPECIES: Species.COHO,
                SurveyDataColumn.DISTANCE: 10,
                SurveyDataColumn.QUANTITY: 1,
                SurveyDataColumn.LENGTH: 12.5,
                SurveyDataColumn.WIDTH: 3.1,
                SurveyDataColumn.PREDATION: PredationStatus.NO,
                SurveyDataColumn.CARCASS_STATE: CarcassState.NO_DAMAGE,
            },
        ),
        (
            {
                "ec5_uuid": "kobo-1",
                "survey_date": "2024-09-15",
                "species": "chum",
                "carcass_age": "12-24 hours",
                "notes": "found near bank",
            },
            {
                SurveyDataColumn.EXTERNAL_ID: "kobo-1",
                SurveyDataColumn.YEAR: 2024,
                SurveyDataColumn.SPECIES: Species.CHUM,
                SurveyDataColumn.CARCASS_AGE_LABEL: "12-24 hours",
                SurveyDataColumn.CARCASS_AGE_MIN: 12,
                SurveyDataColumn.CARCASS_AGE_MAX: 24,
                SurveyDataColumn.NOTE: "found near bank",
            },
        ),
        (
            {
                "ec5_uuid": "csv-1",
                "survey_date": "2018-06-01",
                "species": "coho",
                "quantity": "2",
                "Location": "49.123 -123.456",
            },
            {
                SurveyDataColumn.EXTERNAL_ID: "csv-1",
                SurveyDataColumn.YEAR: 2018,
                SurveyDataColumn.SPECIES: Species.COHO,
                SurveyDataColumn.QUANTITY: 2,
                SurveyDataColumn.LATITUDE: 49.123,
                SurveyDataColumn.LONGITUDE: -123.456,
            },
        ),
    ],
)
def test_process_entry_blob_sample_blobs(blob, expected):
    processor = SurveyDataEntryProcessor()
    entry = processor.process_entry_blob(blob)

    for field, value in expected.items():
        assert getattr(entry, field) == value


@pytest.mark.parametrize(
    "blob, expected",
    [
        (
            {"ec5_uuid": "qty-1", "quantity": "", "species": "coho"},
            {SurveyDataColumn.QUANTITY: 1},
        ),
        (
            {"ec5_uuid": "qty-2", "quantity": "3", "species": "coho"},
            {SurveyDataColumn.QUANTITY: 3},
        ),
        (
            {
                "ec5_uuid": "loc-1",
                "Location": "49.123 -123.456",
                "carcass_location": "in creek",
            },
            {
                SurveyDataColumn.LATITUDE: 49.123,
                SurveyDataColumn.LONGITUDE: -123.456,
                SurveyDataColumn.LOCATION: CarcassLocation.IN_CREEK,
            },
        ),
        (
            {
                "ec5_uuid": "age-1",
                "carcass_age": "1-12 hours",
                "location": {"latitude": 49.0, "longitude": -123.456, "accuracy": 12.0},
            },
            {
                SurveyDataColumn.CARCASS_AGE_LABEL: "1-12 hours",
                SurveyDataColumn.CARCASS_AGE_MIN: 1,
                SurveyDataColumn.CARCASS_AGE_MAX: 12,
                SurveyDataColumn.LATITUDE: 49.0,
                SurveyDataColumn.LONGITUDE: -123.456,
                SurveyDataColumn.ACCURACY: 12.0,
            },
        ),
        (
            {"ec5_uuid": "pred-1", "predation": "no damage"},
            {
                SurveyDataColumn.PREDATION: PredationStatus.NO,
                SurveyDataColumn.CARCASS_STATE: CarcassState.NO_DAMAGE,
            },
        ),
        (
            {"_id": "external-1", "notes": "note1", "predation": "y/n"},
            {
                SurveyDataColumn.EXTERNAL_ID: "external-1",
                SurveyDataColumn.NOTE: "note1; original predation status: y/n",
                SurveyDataColumn.PREDATION: PredationStatus.SCAVENGED,
                SurveyDataColumn.CARCASS_STATE: CarcassState.DAMAGED,
            },
        ),
    ],
)
def test_process_entry_blob_special_cases(blob, expected):
    processor = SurveyDataEntryProcessor()
    entry = processor.process_entry_blob(blob)

    for field, value in expected.items():
        assert getattr(entry, field) == value


def test_process_entry_blob_uses_parent_uuid_date_lookup():
    processor = SurveyDataEntryProcessor()
    processor.survey_dates_map = {"parent-1": "2024-09-15"}

    entry = processor.process_entry_blob(
        {"ec5_uuid": "entry-1", "ec5_parent_uuid": "parent-1", "species": "chum"}
    )

    assert entry.external_id == "entry-1"
    assert entry.survey_date == datetime(2024, 9, 15)
    assert entry.year == 2024
    assert entry.species == Species.CHUM
