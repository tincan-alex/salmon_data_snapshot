from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

# data operation and source
class DataOperation(StrEnum):
    # pull json data from urls, create new directory in data_snapshots
    SNAPSHOT = "snapshot"
    # create db from latest directory in data_snapshots
    PROCESS = "process"
    # SNAPSHOT + PROCESS
    INGEST = "snapshot"
    # run validation on DB
    VALIDATE = "validate"

class DataType(StrEnum):
    DATES = "dates"
    SURVEY = "survey"

class DataSourceType(StrEnum):
    EPICOLLECT = "epicollect"
    KOBOTOOLBOX = "kobotoolbox"

@dataclass
class DataSource:
    source_type: DataSourceType
    data_type: DataType
    year: int
    url: str

@dataclass
class DataOrchestratorConfig:
    operation: DataOperation
    data_sources: list[DataSource]
    # used for INGEST and PROCESS - when set to true, search past snapshots for data from previous years and attempt to upsert them
    process_legacy_data: Optional[bool]
