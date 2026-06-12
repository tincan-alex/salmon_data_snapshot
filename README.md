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
* ask about how to handle certain values
    * is there "unknown" in e.g. sex/predation/adipose fin status or should they all be left blank?
    * how should "-" be treated? should they be filtered/blanked out?
    * it looks like there is scavenged status in predation field in scanned data - it doesn't seem to be the case in epicollect/kobotoolbox data; how should eye loss/eye loss only values in predation be treated?
    * there are some values in predation field that i'm not quite sure what they mean, they are mostly present in 2017 and 2018 data - y/n, y/p, n/y, p/s, s/p, s/y, y/p
    * should we keep data like carcass age and length/width?
* unit tests
* github action for survey season daily ingestion
    * rebase from master
    * run ingest on latest survey data source
    * if no exception during validation, auto commit push to live_update remote branch