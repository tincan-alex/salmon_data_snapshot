from src.data_access.constructs import SURVEY_DATA_COLUMNS_TO_TYPE, SURVEY_DATA_TABLE_NAME

DROP_TABLE_QUERY = f'''
    DROP TABLE IF EXISTS {SURVEY_DATA_TABLE_NAME};
'''

def create_table_query():
    return f'''
        CREATE TABLE IF NOT EXISTS {SURVEY_DATA_TABLE_NAME} (
            {', '.join([f"{c} {t}" for c, t in SURVEY_DATA_COLUMNS_TO_TYPE.items()])}
        );
    '''

def insert_row_query():
    return f'''
        INSERT OR IGNORE INTO {SURVEY_DATA_TABLE_NAME} (
            {', '.join(SURVEY_DATA_COLUMNS_TO_TYPE.keys())}
        ) VALUES (?, ?, ?, ?, ?, ?, COALESCE(?,1), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''

def upsert_row_query():
    return f'''
        INSERT INTO {SURVEY_DATA_TABLE_NAME} (
            {', '.join(SURVEY_DATA_COLUMNS_TO_TYPE.keys())}
        ) VALUES (?, ?, ?, ?, ?, ?, COALESCE(?,1), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            {', '.join([f"{c} = excluded.{c}" for c in SURVEY_DATA_COLUMNS_TO_TYPE.keys()])}
        ;
    '''
