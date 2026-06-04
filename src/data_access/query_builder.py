from src.data_access.constructs import SurveyData


CREATE_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS survey_data (
        _id STRING PRIMARY KEY,
        survey_date DATE,
        year DATE,
        quantity INTEGER,
        distance INTEGER,
        stream TEXT,
        type TEXT,
        species TEXT,
        predation TEXT,
        length FLOAT,
        width FLOAT,
        spawned TEXT,
        sex TEXT,
        latitude FLOAT,
        longitude FLOAT,
        accuracy FLOAT
    );
'''

DROP_TABLE_QUERY = '''
    DROP TABLE IF EXISTS survey_data;
'''

INSERT_SURVEY_DATA_QUERY = '''
    INSERT OR IGNORE INTO survey_data (
    _id,
    Survey_Date,
    year,
    Quantity,
    Distance,
    Stream,
    Type,
    Species,
    Predation,
    Length,
    Width,
    Spawned,
    Sex,
    Latitude,
    Longitude,
    Accuracy
    ) VALUES (?, ?, ?, COALESCE(?,1), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
'''

def convert_data_for_insert(data: SurveyData):
    pass