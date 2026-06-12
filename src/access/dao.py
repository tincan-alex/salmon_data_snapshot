from src.access.constructs import SurveyData
from sqlite3 import Connection

from src.access.query_builder import (
    DROP_TABLE_QUERY,
    create_table_query,
    insert_row_query,
    upsert_row_query,
)


class SurveyDataDao:
    def __init__(self, db_connection: Connection):
        self.conn = db_connection

    def insert(self, data: SurveyData):
        self.conn.execute(insert_row_query(), data.to_db_values())

    def upsert(self, data: SurveyData):
        self.conn.execute(upsert_row_query(), data.to_db_values())

    def query(self, query: str) -> list:
        return self.conn.execute(query).fetchall()

    def create_table(self):
        self.conn.execute(create_table_query())

    def create_indices(self):
        pass

    def clean(self):
        self.conn.execute(DROP_TABLE_QUERY)
