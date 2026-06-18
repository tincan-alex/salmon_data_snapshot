from src.access.dao import SurveyDataDao
from src.constructs import DataOrchestratorConfig, DataOperation
from src.orchestrator import DataOrchestrator
from src.validation.validator import SurveyDataValidator


def test_orchestrator_ingest_from_snapshot_and_validate(
    temp_db_path, sqlite_connection, prod_stats
):
    """End-to-end test: run orchestrator ingest on temp DB with latest snapshot, validate against prod db."""
    orchestrator = DataOrchestrator()
    orchestrator.db_path = temp_db_path
    config = DataOrchestratorConfig(operation=DataOperation.INGEST)
    orchestrator.run_operation(config)

    dao = SurveyDataDao(sqlite_connection)
    validator = SurveyDataValidator(dao)
    validator.validate_db(prod_stats)


def test_orchestrator_ingest_and_rebuild_from_snapshot(
    temp_db_path, sqlite_connection, prod_stats
):
    """End-to-end test: run orchestrator ingest on temp DB and rebuild from all data, validate against prod db."""
    orchestrator = DataOrchestrator()
    orchestrator.db_path = temp_db_path
    config = DataOrchestratorConfig(operation=DataOperation.INGEST, rebuild_db=True)
    orchestrator.run_operation(config)

    dao = SurveyDataDao(sqlite_connection)
    validator = SurveyDataValidator(dao)
    validator.validate_db(prod_stats)
