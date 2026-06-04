from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Optional


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
    survey_date: Optional[datetime]
    survey_type: Optional[SurveyType]
    distance: Optional[int]
    stream: Optional[StreamLabel]
    species: Optional[str]
    quantity: Optional[int]
    sex: Optional[Sex]
    life_stage: Optional[str]
    adipose_fin: Optional[AdiposeFinStatus]
    length: Optional[float]
    width: Optional[float]
    carcass_age_label: Optional[str]
    carcass_age_min: Optional[int]
    carcass_age_max: Optional[int]
    spawned: Optional[SpawnStatus]
    predation: Optional[PredationStatus]
    latitude: Optional[float]
    longitude: Optional[float]
    accuracy: Optional[float]
    note: Optional[str]
