WRI ETL
========

A db seeder etl tool for wri data.

### Setup
1. execute `scripts\create_db.sql`
1. execute `scripts\create_tables.sql`
1. see usage

### Model Schema
- The key values are the source table attributes
- the values contain the information about the etl process
    - type is the field type. Used for casting
    - map is the destination field
    - order is to sync the order for querying, inserting, and updating
    - value is used on unmappable fields
    - action is a thing applied to the value
- fields prefixed with `*` are not found in the source and are expected to have a `value` property to insert into that field on the destintation table.
- fields prefeixed with `!` are duplicated where you need to act on the same field twice

### Usage
from the **/src** directory

`python -m dbseeder seed "connections\WRI on PROD.sde" "connections\WRI on (local).sde" "http://localhost/wri/"`

### Tests
from the **parent** project directory
`tox`

### Problems
