# collect and combine salmon survey data
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

from src.constructs import DataOperation, DataOrchestratorConfig, DataSource
from src.access.dao import SurveyDataDao
from src.process.ingester import SurveyDataIngester
from src.process.processor import SurveyDataProcessor
from src.validation.validator import SurveyDataValidator


class DataOrchestrator:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.db_path = self.base_dir / "survey_data.db"
        self.snapshot_root = Path(self.base_dir / "data_snapshots")
        snapshot_dirs = [p for p in self.snapshot_root.iterdir() if p.is_dir()]
        self.snapshot_path = max(snapshot_dirs, key=lambda p: p.name)
        print(f"Latest snapshot: {self.snapshot_path}")

    def run_operation(self, config: DataOrchestratorConfig):
        print(f"Running operation with config {config}...")
        self.config = config
        match self.config.operation:
            case DataOperation.INGEST:
                self.ingest_data()
            case DataOperation.VALIDATE:
                self.validate_data()

    def ingest_data(self):
        if self.config.data_sources:
            self.create_data_snapshot()

        with sqlite3.connect(self.db_path, autocommit=False) as conn:
            survey_dao = SurveyDataDao(conn)
            validator = SurveyDataValidator(survey_dao)
            processor = SurveyDataProcessor(survey_dao)

            self.yearly_info_snapshot = validator.get_survey_data_yearly_stats()
            if self.config.rebuild_db:
                survey_dao.clean()
            survey_dao.create_table()
            survey_dao.create_indices()

            if self.config.rebuild_db or self.config.years_to_process:
                processor.process_all_data(
                    self.snapshot_root, self.config.years_to_process
                )
                print(
                    f"PROCESSED LATEST DATA for {self.config.years_to_process if self.config.years_to_process else 'all years'}"
                )
            else:
                processor.process_path(self.snapshot_path)
                print(f"PROCESSED DATA at {self.snapshot_path}")

            validator.validate_db(self.yearly_info_snapshot)
            print(f"VALIDATED survey data at {self.db_path}")

    def create_data_snapshot(self):
        snapshot_dir = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S.%fZ")
        self.snapshot_path = self.snapshot_root / snapshot_dir
        self.snapshot_path.mkdir(parents=True, exist_ok=True)
        ingester = SurveyDataIngester(self.config.data_sources, self.snapshot_path)
        ingester.ingest_data()
        print(f"GENERATED SNAPSHOT at {self.snapshot_path}")

    def validate_data(self):
        with sqlite3.connect(self.db_path) as conn:
            survey_dao = SurveyDataDao(conn)
            validator = SurveyDataValidator(survey_dao)
            validator.validate_db()
        print(f"VALIDATED survey data at {self.db_path}")


def parse_config_from_args(args: argparse.Namespace) -> DataOrchestratorConfig:
    data_sources = []
    if args.data_sources_path:
        blob = json.load(open(args.data_sources_path))
        if isinstance(blob, list):
            data_sources = [
                DataSource(
                    source_type=source["source_type"],
                    data_type=source["data_type"],
                    year=source["year"],
                    url=source["url"],
                )
                for source in blob
            ]
    return DataOrchestratorConfig(
        operation=args.operation,
        rebuild_db=args.rebuild_db,
        data_sources=data_sources,
        years_to_process=args.years,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest salmon survey data to update survey_data.db"
    )
    parser.add_argument(
        "--operation",
        type=DataOperation,
        default=DataOperation.VALIDATE,
        help="Specify to ingest or validate data.",
    )
    parser.add_argument(
        "--rebuild-db",
        type=bool,
        default=False,
        help="Set to true if rebuilding database.",
    )
    parser.add_argument(
        "--years",
        nargs="+",
        type=int,
        default=[],
        help="Specify list of years of survey data to process if only processing specific years of data.",
    )
    parser.add_argument(
        "--data-sources-path",
        type=Path,
        default=None,
        help="Specify path to JSON list of data sources if ingesting data.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = parse_config_from_args(args)
    orchestrator = DataOrchestrator()
    orchestrator.run_operation(config)


if __name__ == "__main__":
    main()
