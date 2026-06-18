salmon_data_snapshot

This repo pulls Carkeek salmon survey data across epicollect and kobotoolbox, normalizes data from both and combines it
into `survey_data.db`.

=======================================================================================================================

USAGE:

```
python -m src.orchestrator --help                                                                       
usage: python.exe -m src.orchestrator [-h] [--operation OPERATION] [--rebuild-db REBUILD_DB] [--years YEARS [YEARS ...]] [--data-sources-path DATA_SOURCES_PATH]

Ingest salmon survey data to update survey_data.db

options:
  -h, --help            show this help message and exit
  --operation OPERATION
                        Specify to ingest or validate data.
  --rebuild-db REBUILD_DB
                        Set to true if rebuilding database.
  --years YEARS [YEARS ...]
                        Specify list of years of survey data to process if only processing specific years of data.
  --data-sources-path DATA_SOURCES_PATH
                        Specify path to JSON list of data sources if ingesting data.
```

SAMPLE COMMANDS:
* Ingest data from latest source into database

`python -m src.orchestrator --operation ingest --data-sources-path .\configs\latest_data_source.json`

* Ingest all data from source into database

`python -m src.orchestrator --operation ingest --data-sources-path .\configs\all_data_sources.json`

* Rebuild the database from existing snapshots

`python -m src.orchestrator --operation ingest --rebuild-db true`

* Ingest the years of data from 2015 to 2018 from existing snapshots (latest preferred for each year) into database

`python -m src.orchestrator --operation ingest --years 2015 2016 2017 2018`

* Run validation on the current database

`python -m src.orchestrator --operation validate`


=======================================================================================================================

TODO:
* unit tests
    * set up in memory db and orchestrator
        * run assertions on yearly info
        * run full db rebuild from all data snapshot
        * run validation, ensure no errors
    * SurveyDataEntryProcessor unit tests for different cases