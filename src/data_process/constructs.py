from src.data_access.constructs import SurveyDataColumn, SurveyType, StreamLabel, Species, Sex, LifeStage, AdiposeFinStatus, SpawnStatus, PredationStatus

SURVEY_DATA_POTENTIAL_VALUES_MAP = {
    SurveyDataColumn.SURVEY_TYPE: {
        SurveyType.LIVE: {"live", "l"},
        SurveyType.DEAD: {"dead", "d"},
        SurveyType.REMNANT: {"remnant", "r"},
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
        LifeStage.JUNIOR: {"junior", "j", "ju"},
        LifeStage.FIRST_YEAR: {"1st year", "1", "1yr"},
        LifeStage.SECOND_YEAR: {"2nd year", "2", "2 yr"},
        LifeStage.THIRD_YEAR: {"3rd year", "3", "3 yr"},
        LifeStage.UNKNOWN: {"unknown", "u", "unk", "uk"},
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
        PredationStatus.EYE_LOSS_ONLY: {"eye loss only"},
        PredationStatus.UNKNOWN: {"unknown", "u", "unk", "uk"},
    },
}

SURVEY_DATA_POTENTIAL_KEYS_MAP = {
    SurveyDataColumn.ID: {"_id", "ec5_uuid"},
    SurveyDataColumn.SURVEY_DATE: {"Survey_Date"},
    SurveyDataColumn.SURVEY_TYPE: {"Type"},
    SurveyDataColumn.DISTANCE: {"Distance"},
    SurveyDataColumn.STREAM: {"Stream"},
    SurveyDataColumn.SPECIES: {"Species"},
    SurveyDataColumn.QUANTITY: {"Quantity"},
    SurveyDataColumn.SEX: {"Sex"},
    SurveyDataColumn.LIFE_STAGE: {"Life_Stage"},
    SurveyDataColumn.ADIPOSE_FIN: {"Adipose_Fin"},
    SurveyDataColumn.LENGTH: {"Length_Inches", "Length"},
    SurveyDataColumn.WIDTH: {"Width_Inches", "Width"},
    SurveyDataColumn.CARCASS_AGE_LABEL: {"Carcass_Age", "Hours_Since_Death"},
    SurveyDataColumn.SPAWNED: {"Spawning_Success", "Spawned"},
    SurveyDataColumn.PREDATION: {"Predation"},
    SurveyDataColumn.NOTE: {"Notes"},
}
