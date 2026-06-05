# collect and combine salmon survey data
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

from src.constructs import DataOperation, DataOrchestratorConfig, DataSource
from src.data_access.dao import SurveyDataDao
from src.data_process.ingester import SurveyDataIngester
from src.data_process.processor import SurveyDataProcessor

class DataOrchestrator:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent
        self.db_path = base_dir / "src" / "survey_data.db"
        self.snapshot_root = Path(base_dir / "src" / "data_snapshots")
        snapshot_dirs = [p for p in self.snapshot_root.iterdir() if p.is_dir()]
        self.snapshot_path = max(snapshot_dirs, key=lambda p: p.name)
        print(f"Latest snapshot: {self.snapshot_path}")
    
    def run_operation(self, config_path: str):
        self.config = self._parse_config_from_json(config_path)
        match self.config.operation:
            case DataOperation.SNAPSHOT:
                self.create_data_snapshot()
            case DataOperation.PROCESS:
                self.process_data()
            case DataOperation.INGEST:
                self.ingest_data()
            case DataOperation.VALIDATE:
                self.validate_data()

    def create_data_snapshot(self):
        # in self.snapshot_path, loop through each data source, pull json, write json file to year_datatype.json
        snapshot_dir = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S.%fZ")
        self.snapshot_path = self.snapshot_root / snapshot_dir
        self.snapshot_path.mkdir(parents=True, exist_ok=True)
        ingester = SurveyDataIngester(self.config.data_sources, self.snapshot_path)
        ingester.ingest()

    def process_data(self):
        with sqlite3.connect(self.db_path) as conn:
            survey_dao = SurveyDataDao(conn)
            if self.config.process_legacy_data:
                survey_dao.clean()
            survey_dao.create_table()
            survey_dao.create_indices()
            processor = SurveyDataProcessor(survey_dao)
            processor.process_path(self.snapshot_path)

    def validate_data(self):
        with sqlite3.connect(self.db_path) as conn:
            survey_dao = SurveyDataDao(conn)
            survey_dao.query('validation query')
            # run validations on db

    def ingest_data(self):
        if self.config.data_sources:
            self.create_data_snapshot()
        self.process_data()
        self.validate_data()
    
    def _parse_config_from_json(self, config_path: str):
        config_blob = json.load(open(config_path))
        data_sources = [
            DataSource(
                source_type=source["source_type"],
                data_type=source["data_type"],
                year=source['year'],
                url=source['url']
            )
            for source in config_blob.get('data_sources')
        ] if config_blob.get('data_sources') else []
        return DataOrchestratorConfig(
            operation=config_blob['operation'],
            process_legacy_data=config_blob.get('process_legacy_data', False),
            data_sources=data_sources
        )

