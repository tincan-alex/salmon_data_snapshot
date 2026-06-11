salmon_data_snapshot

This repo pulls Carkeek salmon survey data across epicollect and kobotoolbox, normalizes data from both and combines it
into `survey_data.db`.

=======================================================================================================================

USAGE:

```
python -m src.orchestrator --help                                                                       
usage: python.exe -m src.orchestrator [-h] [--operation OPERATION] [--process-legacy-data PROCESS_LEGACY_DATA] [--years YEARS [YEARS ...]]
                                      [--data-sources-path DATA_SOURCES_PATH]

Pull and/or process salmon survey data to update survey_data.db

options:
  -h, --help            show this help message and exit
  --operation OPERATION
                        Specify to snapshot, process, ingest, or validate.
  --process-legacy-data PROCESS_LEGACY_DATA
                        Set to true if rebuilding database and processing legacy data from previous snapshots.
  --years YEARS [YEARS ...]
                        Specify list of years of survey data to process when rebuilding database with legacy data from previous snapshots.
  --data-sources-path DATA_SOURCES_PATH
                        Path to JSON list of data sources.
```

SAMPLE COMMANDS
* Ingest the latest data into database and run validation
`python -m src.orchestrator --operation ingest --data-sources-path .\configs\latest_data_sources.json`

* Create a snapshot from all data sources under `data_snapshots`, but don't insert into database
`python -m src.orchestrator --operation snapshot --data-sources-path .\configs\all_data_sources.json`

* Process the latest data snapshot, insert into database, and run validation
`python -m src.orchestrator --operation process`

* Process the years of data from 2019 to 2025 from existing snapshots (latest preferred for each year), insert into database, and run validation
`python -m src.orchestrator --operation process --process-legacy-data true --years 2019 2020 2021 2022 2023 2024 2025`

* Only run validation on the current database
`python -m src.orchestrator --operation validate`


=======================================================================================================================

todo:
* assign internal id with external id uniqueness index
* add pebble column
* support csv ingestion
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