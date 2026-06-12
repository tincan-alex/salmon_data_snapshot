from src.access.constructs import SURVEY_DATA_COLUMNS_TO_TYPE, SURVEY_DATA_TABLE_NAME
from src.access.constructs import SurveyDataColumn

DROP_TABLE_QUERY = f"""
    DROP TABLE IF EXISTS {SURVEY_DATA_TABLE_NAME};
"""


def create_table_query():
    return f"""
        CREATE TABLE IF NOT EXISTS {SURVEY_DATA_TABLE_NAME} (
            {', '.join([f"{c} {t}" for c, t in SURVEY_DATA_COLUMNS_TO_TYPE.items()])}
        );
    """


def insert_row_query():
    return f"""
        INSERT OR IGNORE INTO {SURVEY_DATA_TABLE_NAME} (
            {', '.join(SURVEY_DATA_COLUMNS_TO_TYPE.keys())}
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE(?,1), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """


def upsert_row_query():
    return f"""
        INSERT INTO {SURVEY_DATA_TABLE_NAME} (
            {', '.join(SURVEY_DATA_COLUMNS_TO_TYPE.keys())}
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE(?,1), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(external_id) DO UPDATE SET
            {', '.join([f"{c} = excluded.{c}" for c in SURVEY_DATA_COLUMNS_TO_TYPE.keys() if c != SurveyDataColumn.EXTERNAL_ID])}
        ;
    """


def value_count_query(column, value, year=None):
    return f"""
        SELECT COALESCE(SUM(CASE WHEN {column} = {value} THEN quantity END), 0) AS count FROM {SURVEY_DATA_TABLE_NAME}
            {f"WHERE {SurveyDataColumn.YEAR} = {year}" if year else ""}
        ;
    """


def distinct_counts_query(column, year=None):
    return f"""
        SELECT {column}, COALESCE(SUM(quantity), 0) AS count FROM {SURVEY_DATA_TABLE_NAME}
            {f"WHERE {SurveyDataColumn.YEAR} = {year}" if year else ""}
        GROUP BY {column};
    """


def presence_count_query(column, year=None):
    return f"""
        SELECT COALESCE(SUM(CASE WHEN {column} IS NOT NULL AND {column} NOT IN (0, '') THEN quantity END), 0) AS count FROM {SURVEY_DATA_TABLE_NAME}
            {f"WHERE {SurveyDataColumn.YEAR} = {year}" if year else ""}
        ;
    """
