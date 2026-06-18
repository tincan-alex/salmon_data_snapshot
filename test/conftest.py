from pathlib import Path
import shutil
import sqlite3
from src.access.dao import SurveyDataDao

import pytest

from src.validation.validator import SurveyDataValidator


@pytest.fixture
def repo_root():
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def repo_db_path(repo_root):
    return repo_root / "survey_data.db"


@pytest.fixture
def temp_db_path(repo_db_path, tmp_path):
    destination = tmp_path / "test.db"
    shutil.copy(repo_db_path, destination)
    return destination


@pytest.fixture
def sqlite_connection(tmp_path):
    db_path = tmp_path / "test.db"
    connection = sqlite3.connect(db_path)
    yield connection
    connection.close()


@pytest.fixture
def survey_data_dao(sqlite_connection):
    dao = SurveyDataDao(sqlite_connection)
    dao.create_table()
    return dao


@pytest.fixture
def prod_stats(repo_db_path):
    uri = f"file:{repo_db_path}?mode=ro"
    with sqlite3.connect(uri, uri=True) as conn:
        validator = SurveyDataValidator(survey_data_dao=SurveyDataDao(conn))
        return validator.get_survey_data_yearly_stats()
