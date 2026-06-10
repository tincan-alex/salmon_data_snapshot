from dataclasses import dataclass, field
from enum import StrEnum

# data operation and source
class DataOperation(StrEnum):
    # pull json data from urls, create new directory in data_snapshots
    SNAPSHOT = "snapshot"
    # create db from latest directory in data_snapshots
    PROCESS = "process"
    # SNAPSHOT + PROCESS
    INGEST = "ingest"
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
    data_sources: list[DataSource]=field(default_factory=list)

    # used for INGEST and PROCESS - when set to true, search past snapshots for data from previous years and attempt to upsert them
    process_legacy_data: bool=False
    # required when process_legacy_data is true - specify years to search past snapshots for
    years_to_process: list[int]=field(default_factory=list) 
