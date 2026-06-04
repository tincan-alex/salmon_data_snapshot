from src.data_access.constructs import SurveyData
from sqlite3 import Connection

from src.data_access.query_builder import CREATE_TABLE_QUERY, DROP_TABLE_QUERY, INSERT_SURVEY_DATA_QUERY


class SurveyDataDao:
    def __init__(self, db_connection: Connection):
        self.conn = db_connection

    def insert(self, data: SurveyData):
        self.conn.execute(INSERT_SURVEY_DATA_QUERY, data)

    def query(self, query: str):
        self.conn.execute(query)

    def create_table(self):
        self.conn.execute(CREATE_TABLE_QUERY)
        self.conn.commit()

    def create_indices(self):
        pass

    def clean(self):
        self.conn.execute(DROP_TABLE_QUERY)
        self.conn.commit()