from enum import StrEnum

from src.access.constructs import AdiposeFinStatus, PredationStatus, SpawnStatus

class SurveyDataAssertion(StrEnum):
    EXPECTED_LIVE_COUNT = "expected_live_count"
    EXPECTED_DEAD_COUNT = "expected_dead_count"
    EXPECTED_REDD_COUNT = "expected_redd_count"
    EXPECTED_CHUM_COUNT = "expected_chum_count"
    EXPECTED_COHO_COUNT = "expected_coho_count"
    ADIPOSE_FIN_STATUSES = "adipose_fin_statuses"
    PREDATION_STATUSES = "predation_statuses"
    SPAWN_STATUSES = "spawn_statuses"
    ENTRY_WITH_NOTES = "entry_with_notes"
    ENTRY_WITH_DISTANCE = "entry_with_distance"
    ENTRY_WITH_LOCATION = "entry_with_location"
    ENTRY_ON_PIPERS_CREEK = "entry_on_pipers_creek"

SURVEY_DATA_PRESENCE_ASSERTIONS = [
    SurveyDataAssertion.ENTRY_WITH_NOTES,
    SurveyDataAssertion.ENTRY_WITH_DISTANCE,
    SurveyDataAssertion.ENTRY_WITH_LOCATION,
    SurveyDataAssertion.ENTRY_ON_PIPERS_CREEK,
]

SURVEY_DATA_DISTINCT_VALUE_ASSERTIONS = {
    SurveyDataAssertion.ADIPOSE_FIN_STATUSES: [status.value for status in AdiposeFinStatus],
    SurveyDataAssertion.PREDATION_STATUSES: [status.value for status in PredationStatus],
    SurveyDataAssertion.SPAWN_STATUSES: [status.value for status in SpawnStatus],
}

SURVEY_DATA_EXPECTED_COUNTS_MAP = {
    2019: {
        SurveyDataAssertion.EXPECTED_LIVE_COUNT: 70,
        SurveyDataAssertion.EXPECTED_DEAD_COUNT: 74,
        SurveyDataAssertion.EXPECTED_REDD_COUNT: 0,
        SurveyDataAssertion.EXPECTED_CHUM_COUNT: 101,
        SurveyDataAssertion.EXPECTED_COHO_COUNT: 24,
    },
    2020: {
        SurveyDataAssertion.EXPECTED_LIVE_COUNT: 413,
        SurveyDataAssertion.EXPECTED_DEAD_COUNT: 215,
        SurveyDataAssertion.EXPECTED_REDD_COUNT: 0,
        SurveyDataAssertion.EXPECTED_CHUM_COUNT: 582,
        SurveyDataAssertion.EXPECTED_COHO_COUNT: 14,
    },
    2021: {
        SurveyDataAssertion.EXPECTED_LIVE_COUNT: 2242,
        SurveyDataAssertion.EXPECTED_DEAD_COUNT: 1005,
        SurveyDataAssertion.EXPECTED_REDD_COUNT: 108,
        SurveyDataAssertion.EXPECTED_CHUM_COUNT: 3138,
        SurveyDataAssertion.EXPECTED_COHO_COUNT: 80,
    },
    2022: {
        SurveyDataAssertion.EXPECTED_LIVE_COUNT: 2635,
        SurveyDataAssertion.EXPECTED_DEAD_COUNT: 1135,
        SurveyDataAssertion.EXPECTED_REDD_COUNT: 48,
        SurveyDataAssertion.EXPECTED_CHUM_COUNT: 3549,
        SurveyDataAssertion.EXPECTED_COHO_COUNT: 213,
    },
    2023: {
        SurveyDataAssertion.EXPECTED_LIVE_COUNT: 756,
        SurveyDataAssertion.EXPECTED_DEAD_COUNT: 343,
        SurveyDataAssertion.EXPECTED_REDD_COUNT: 33,
        SurveyDataAssertion.EXPECTED_CHUM_COUNT: 991,
        SurveyDataAssertion.EXPECTED_COHO_COUNT: 42,
    },
    2024: {
        SurveyDataAssertion.EXPECTED_LIVE_COUNT: 6012,
        SurveyDataAssertion.EXPECTED_DEAD_COUNT: 3124,
        SurveyDataAssertion.EXPECTED_REDD_COUNT: 53,
        SurveyDataAssertion.EXPECTED_CHUM_COUNT: 8961,
        SurveyDataAssertion.EXPECTED_COHO_COUNT: 141,
    },
    2025: {
        SurveyDataAssertion.EXPECTED_LIVE_COUNT: 846,
        SurveyDataAssertion.EXPECTED_DEAD_COUNT: 440,
        SurveyDataAssertion.EXPECTED_REDD_COUNT: 43,
        SurveyDataAssertion.EXPECTED_CHUM_COUNT: 1246,
        SurveyDataAssertion.EXPECTED_COHO_COUNT: 22,
    },
}