from dataclasses import dataclass, field
from enum import StrEnum


# data operation and source
class DataOperation(StrEnum):
    INGEST = "ingest"
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
    data_sources: list[DataSource] = field(default_factory=list)
    rebuild_db: bool = False
    years_to_process: list[int] = field(default_factory=list)
