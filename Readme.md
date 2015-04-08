WRI ETL
========

A db seeder etl tool for wri data.

### Setup
1. execute `scripts\create_db.sql`
1. execute `scripts\create_tables.sql`
1. enable SDE
1. register tables with database
1. see usage

### Tests
`tox`

### Problems
`expecting string data` means the lookup value was not in the models table. Change batch size to 2 and look for a number where there should be a value. Add the number: None

`string or binary data to be truncated` - run `python -m dbseeder path/to/csv's --length` and adjust sql schema 

### Usage
`cd c:\Projects\GitHub\wri-db\src`

`python -m dbseeder seed "C:\Projects\GitHub\wri-db\src\dbseeder\connections\WRI on itdb104sp.dts.utah.gov.sde" "C:\Projects\GitHub\wri-db\src\dbseeder\connections\WRI_Spatial on (local).sde"`