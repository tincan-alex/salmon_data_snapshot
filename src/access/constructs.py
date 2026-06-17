from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Optional, OrderedDict

SURVEY_DATA_TABLE_NAME = "survey_data"


class SurveyDataColumn(StrEnum):
    ID = "id"
    EXTERNAL_ID = "external_id"
    SURVEY_DATE = "survey_date"
    YEAR = "year"
    SURVEY_TYPE = "survey_type"
    DISTANCE = "distance"
    STREAM = "stream"
    SPECIES = "species"
    GRAVEL = "gravel"
    QUANTITY = "quantity"
    REDD_SUBSTRATE = "redd_substrate"
    SEX = "sex"
    LIFE_STAGE = "life_stage"
    ADIPOSE_FIN = "adipose_fin"
    LENGTH = "length"
    WIDTH = "width"
    CARCASS_AGE_LABEL = "carcass_age_label"
    CARCASS_AGE_MIN = "carcass_age_min"
    CARCASS_AGE_MAX = "carcass_age_max"
    CARCASS_STATE = "carcass_state"
    SPAWNED = "spawned"
    PREDATION = "predation"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    ACCURACY = "accuracy"
    LOCATION = "location"
    NOTE = "note"


SURVEY_DATA_COLUMNS_TO_TYPE: OrderedDict[str, str] = {
    SurveyDataColumn.ID: "INTEGER PRIMARY KEY",
    SurveyDataColumn.EXTERNAL_ID: "TEXT UNIQUE",
    SurveyDataColumn.SURVEY_DATE: "DATE",
    SurveyDataColumn.YEAR: "INTEGER",
    SurveyDataColumn.SURVEY_TYPE: "TEXT",
    SurveyDataColumn.DISTANCE: "INTEGER",
    SurveyDataColumn.STREAM: "TEXT",
    SurveyDataColumn.GRAVEL: "TEXT",
    SurveyDataColumn.SPECIES: "TEXT",
    SurveyDataColumn.QUANTITY: "INTEGER",
    SurveyDataColumn.REDD_SUBSTRATE: "TEXT",
    SurveyDataColumn.SEX: "TEXT",
    SurveyDataColumn.LIFE_STAGE: "TEXT",
    SurveyDataColumn.ADIPOSE_FIN: "TEXT",
    SurveyDataColumn.LENGTH: "FLOAT",
    SurveyDataColumn.WIDTH: "FLOAT",
    SurveyDataColumn.CARCASS_AGE_LABEL: "TEXT",
    SurveyDataColumn.CARCASS_AGE_MIN: "INTEGER",
    SurveyDataColumn.CARCASS_AGE_MAX: "INTEGER",
    SurveyDataColumn.CARCASS_STATE: "TEXT",
    SurveyDataColumn.SPAWNED: "TEXT",
    SurveyDataColumn.PREDATION: "TEXT",
    SurveyDataColumn.LATITUDE: "FLOAT",
    SurveyDataColumn.LONGITUDE: "FLOAT",
    SurveyDataColumn.ACCURACY: "FLOAT",
    SurveyDataColumn.LOCATION: "TEXT",
    SurveyDataColumn.NOTE: "TEXT",
}


class StreamLabel(StrEnum):
    PIPER = "Piper's Creek"
    VENEMA = "Venema Creek"


class SurveyType(StrEnum):
    LIVE = "Live"
    DEAD = "Dead"
    REDD = "Redd"


class Species(StrEnum):
    CHUM = "Chum"
    COHO = "Coho"
    CHINOOK = "Chinook"
    SOCKEYE = "Sockeye"
    SEA_RUN_CUTTHROAT = "Sea-run Cutthroat"
    RESIDENT_CUTTHROAT = "Resident Cutthroat"
    CUTTHROAT = "Cutthroat"
    UNKNOWN = "Unknown"

class ReddSubstrate(StrEnum):
    RIFFLE = "Riffle"
    GRAVEL = "Gravel"


class Sex(StrEnum):
    MALE = "Male"
    FEMALE = "Female"
    UNKNOWN = "Unknown"


class CarcassAge(StrEnum):
    LESS_THAN_1_HOUR = "Less than 1 hour"
    LESS_THAN_12_HOURS = "1-12 hours"
    LESS_THAN_24_HOURS = "12-24 hours"
    GREATER_THAN_24_HOURS = "Greater than 24 hours"


class CarcassLocation(StrEnum):
    OUTSIDE_OF_CREEK = "Outside of creek"
    ON_CREEK_BANK = "On creek bank"
    IN_CREEK = "In creek"


class AdiposeFinStatus(StrEnum):
    YES = "Yes"
    NO = "No"
    UNKNOWN = "Unknown"


class CarcassState(StrEnum):
    DAMAGED = "Damaged"
    NO_DAMAGE = "No damage"
    EYE_LOSS = "Eye loss"
    UNKNOWN = "Unknown"

class PredationStatus(StrEnum):
    PREDATED = "Predated"
    SCAVENGED = "Scavenged"
    BOTH = "Both"
    NO = "No predation"
    UNKNOWN = "Unknown"


class SpawnStatus(StrEnum):
    SPAWNED = "Spawned"
    UNSPAWNED = "Unspawned"
    PARTIAL = "Partially spawned"
    UNKNOWN = "Unknown"


class LifeStage(StrEnum):
    ADULT = "Adult"
    YOUNG = "Young"
    FIRST_YEAR = "1st year"
    SECOND_YEAR = "2nd year"
    THIRD_YEAR = "3rd year"
    UNKNOWN = "Unknown"


@dataclass
class SurveyData:
    external_id: str
    id: Optional[int] = None
    survey_date: Optional[datetime] = None
    survey_type: Optional[SurveyType] = None
    year: Optional[int] = None
    distance: Optional[int] = None
    stream: Optional[StreamLabel] = None
    species: Optional[str] = None
    quantity: Optional[int] = None
    gravel: Optional[str] = None
    redd_substrate: Optional[Sex] = None
    sex: Optional[Sex] = None
    life_stage: Optional[str] = None
    adipose_fin: Optional[AdiposeFinStatus] = None
    length: Optional[float] = None
    width: Optional[float] = None
    carcass_age_label: Optional[str] = None
    carcass_age_min: Optional[int] = None
    carcass_age_max: Optional[int] = None
    carcass_state: Optional[CarcassState] = None
    spawned: Optional[SpawnStatus] = None
    predation: Optional[PredationStatus] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accuracy: Optional[float] = None
    location: Optional[str] = None
    note: Optional[str] = None

    def to_db_values(self):
        values = []
        for c in SURVEY_DATA_COLUMNS_TO_TYPE.keys():
            values.append(getattr(self, c))
        return tuple(values)
