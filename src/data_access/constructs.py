from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Optional, OrderedDict

SURVEY_DATA_TABLE_NAME = 'survey_data'

class SurveyDataColumn(StrEnum):
    ID = "id"
    SURVEY_DATE = "survey_date"
    SURVEY_TYPE = "survey_type"
    DISTANCE = "distance"
    STREAM = "stream"
    SPECIES = "species"
    QUANTITY = "quantity"
    SEX = "sex"
    LIFE_STAGE = "life_stage"
    ADIPOSE_FIN = "adipose_fin"
    LENGTH = "length"
    WIDTH = "width"
    CARCASS_AGE_LABEL = "carcass_age_label"
    CARCASS_AGE_MIN = "carcass_age_min"
    CARCASS_AGE_MAX = "carcass_age_max"
    SPAWNED = "spawned"
    PREDATION = "predation"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    ACCURACY = "accuracy"
    NOTE = "note"


SURVEY_DATA_COLUMNS_TO_TYPE: OrderedDict[str, str] = {
    SurveyDataColumn.ID: "STRING PRIMARY KEY",
    SurveyDataColumn.SURVEY_DATE: "DATE",
    SurveyDataColumn.SURVEY_TYPE: "TEXT",
    SurveyDataColumn.DISTANCE: "INTEGER",
    SurveyDataColumn.STREAM: "TEXT",
    SurveyDataColumn.SPECIES: "TEXT",
    SurveyDataColumn.QUANTITY: "INTEGER",
    SurveyDataColumn.SEX: "TEXT",
    SurveyDataColumn.LIFE_STAGE: "TEXT",
    SurveyDataColumn.ADIPOSE_FIN: "TEXT",
    SurveyDataColumn.LENGTH: "FLOAT",
    SurveyDataColumn.WIDTH: "FLOAT",
    SurveyDataColumn.CARCASS_AGE_LABEL: "TEXT",
    SurveyDataColumn.CARCASS_AGE_MIN: "INTEGER",
    SurveyDataColumn.CARCASS_AGE_MAX: "INTEGER",
    SurveyDataColumn.SPAWNED: "TEXT",
    SurveyDataColumn.PREDATION: "TEXT",
    SurveyDataColumn.LATITUDE: "FLOAT",
    SurveyDataColumn.LONGITUDE: "FLOAT",
    SurveyDataColumn.ACCURACY: "FLOAT",
    SurveyDataColumn.NOTE: "TEXT",
}

class StreamLabel(StrEnum):
    PIPER = "Piper's Creek"
    VENEMA = "Venema Creek"

class SurveyType(StrEnum):
    LIVE = "Live"
    DEAD = "Dead"
    REMNANT = "Remnant"
    REDD = "Redd"

class Species(StrEnum):
    CHUM = "Chum"
    COHO = "Coho"
    CHINOOK = "Chinook"
    SOCKEYE = "Sockeye"
    SEA_RUN_CUTTHROAT = "Sea-run Cutthroat"
    RES_CUTTHROAT = "Resident Cutthroat"
    UNKNOWN = "Unknown"

class Sex(StrEnum):
    MALE = "Male"
    FEMALE = "Female"
    UNKNOWN = "Unknown"

class AdiposeFinStatus(StrEnum):
    YES = "Yes"
    NO = "No"
    UNKNOWN = "Unknown"

class PredationStatus(StrEnum):
    PREDATION = "Predation"
    NO_DAMAGE = "No damage"
    EYE_LOSS_ONLY = "Eye loss only"
    UNKNOWN = "Unknown"

class SpawnStatus(StrEnum):
    SPAWNED = "Spawned"
    UNSPAWNED = "Unspawned"
    PARTIAL = "Partially spawned"
    UNKNOWN = "Unknown"

class LifeStage(StrEnum):
    ADULT = "Adult"
    JUNIOR = "Junior"
    FIRST_YEAR = "1st year"
    SECOND_YEAR = "2nd year"
    THIRD_YEAR = "3rd year"
    UNKNOWN = "Unknown"

@dataclass
class SurveyData:
    id: str
    survey_date: Optional[datetime] = None
    survey_type: Optional[SurveyType] = None
    distance: Optional[int] = None
    stream: Optional[StreamLabel] = None
    species: Optional[str] = None
    quantity: Optional[int] = None
    sex: Optional[Sex] = None
    life_stage: Optional[str] = None
    adipose_fin: Optional[AdiposeFinStatus] = None
    length: Optional[float] = None
    width: Optional[float] = None
    carcass_age_label: Optional[str] = None
    carcass_age_min: Optional[int] = None
    carcass_age_max: Optional[int] = None
    spawned: Optional[SpawnStatus] = None
    predation: Optional[PredationStatus] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accuracy: Optional[float] = None
    note: Optional[str] = None

    def to_db_values(self):
        values = []
        for c in SURVEY_DATA_COLUMNS_TO_TYPE.keys():
            if c == '_id':
                values.append(self.id)
            else:
                values.append(getattr(self, c))
        return tuple(values)


