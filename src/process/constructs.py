from dataclasses import dataclass, field
from pathlib import Path

from src.access.constructs import CarcassAge, SurveyDataColumn, SurveyType, StreamLabel, Species, Sex, LifeStage, AdiposeFinStatus, SpawnStatus, PredationStatus

EPICOLLECT_DELAYS = [5, 60, 120, 300]
DEFAULT_DELAYS = [2, 8, 20]

SURVEY_DATA_POTENTIAL_VALUES_MAP = {
    SurveyDataColumn.SURVEY_TYPE: {
        SurveyType.LIVE: {"live", "l"},
        SurveyType.DEAD: {"dead", "d", "remnant", "r"},
        SurveyType.REDD: {"redd", "red"},
    },
    SurveyDataColumn.STREAM: {
        StreamLabel.PIPER: {"piper", "pipers creek", "piper's creek"},
        StreamLabel.VENEMA: {"venema", "venema creek"},
    },
    SurveyDataColumn.SPECIES: {
        Species.CHUM: {"chum", "ch"},
        Species.COHO: {"coho", "co"},
        Species.CHINOOK: {"chinook", "ck"},
        Species.SOCKEYE: {"sockeye", "so"},
        Species.SEA_RUN_CUTTHROAT: {"sea-run cutthroat"},
        Species.RES_CUTTHROAT: {"resident cutthroat"},
        Species.UNKNOWN: {"unknown", "u", "unk", "uk"},
    },
    SurveyDataColumn.SEX: {
        Sex.MALE: {"male", "m"},
        Sex.FEMALE: {"female", "f"},
        Sex.UNKNOWN: {"unknown", "u", "unk", "uk"},
    },
    SurveyDataColumn.LIFE_STAGE: {
        LifeStage.ADULT: {"adult", "a", "ad"},
        LifeStage.JUVENILE: {"juvenile", "j", "ju"},
        LifeStage.FIRST_YEAR: {"1st year", "1", "1yr", "first year"},
        LifeStage.SECOND_YEAR: {"2nd year", "2", "2 yr", "second year"},
        LifeStage.THIRD_YEAR: {"3rd year", "3", "3 yr", "third year"},
        LifeStage.UNKNOWN: {"unknown", "u", "unk", "uk"},
    },
    SurveyDataColumn.CARCASS_AGE_LABEL: {
        CarcassAge.LESS_THAN_1_HOUR: {"less than 1 hour"},
        CarcassAge.LESS_THAN_12_HOURS: {"1-12 hours"},
        CarcassAge.LESS_THAN_24_HOURS: {"12-24 hours"},
        CarcassAge.GREATER_THAN_24_HOURS: {"greater than 24 hours"},
    },
    SurveyDataColumn.ADIPOSE_FIN: {
        AdiposeFinStatus.YES: {"yes", "y"},
        AdiposeFinStatus.NO: {"no", "n"},
        AdiposeFinStatus.UNKNOWN: {"unknown", "u", "unk", "uk"},
    },
    SurveyDataColumn.SPAWNED: {
        SpawnStatus.SPAWNED: {"spawned", "sp", "s"},
        SpawnStatus.UNSPAWNED: {"unspawned", "us", "uns"},
        SpawnStatus.PARTIAL: {"partially spawned", "ps", "p"},
        SpawnStatus.UNKNOWN: {"unknown", "u", "unk", "uk"},
    },
    SurveyDataColumn.PREDATION: {
        PredationStatus.PREDATION: {"predation", "yes", "y"},
        PredationStatus.NO_DAMAGE: {"no damage", "no", "n"},
        PredationStatus.EYE_LOSS_ONLY: {"eye loss only", "eye loss"},
        PredationStatus.SCAVENGED: {"scavenged", "s", "sc"},
        PredationStatus.UNKNOWN: {"unknown", "u", "unk", "uk"},
    },
}

SURVEY_DATA_POTENTIAL_KEYS_MAP = {
    SurveyDataColumn.EXTERNAL_ID: {"_id", "ec5_uuid", "id"},
    SurveyDataColumn.SURVEY_DATE: {"survey_date"},
    SurveyDataColumn.SURVEY_TYPE: {"type"},
    SurveyDataColumn.DISTANCE: {"distance"},
    SurveyDataColumn.STREAM: {"stream"},
    SurveyDataColumn.SPECIES: {"species"},
    SurveyDataColumn.GRAVEL: {"gravel"},
    SurveyDataColumn.QUANTITY: {"quantity"},
    SurveyDataColumn.SEX: {"sex"},
    SurveyDataColumn.LIFE_STAGE: {"life_stage"},
    SurveyDataColumn.ADIPOSE_FIN: {"adipose_fin"},
    SurveyDataColumn.LENGTH: {"length_inches", "length"},
    SurveyDataColumn.WIDTH: {"width_inches", "width"},
    SurveyDataColumn.CARCASS_AGE_LABEL: {"carcass_age", "hours_since_death"},
    SurveyDataColumn.SPAWNED: {"spawning_success", "spawned"},
    SurveyDataColumn.PREDATION: {"predation"},
    SurveyDataColumn.NOTE: {"notes"},
}

CARCASS_AGE_RANGE_MAP = {
    CarcassAge.LESS_THAN_1_HOUR: (0, 1),
    CarcassAge.LESS_THAN_12_HOURS: (1, 12),
    CarcassAge.LESS_THAN_24_HOURS: (12, 24),
    CarcassAge.GREATER_THAN_24_HOURS: (24, None),
}

@dataclass
class DataForYear:
    year: int
    snapshot: str
    dates_files: list[Path]=field(default_factory=list)
    data_files: list[Path]=field(default_factory=list)
