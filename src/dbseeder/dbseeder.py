#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
dbseeder
----------------------------------
the dbseeder module
'''

import arcpy
from functools import partial
from models import TreatmentArea, Lookup


class Seeder(object):

    def __init__(self):
        super(Seeder, self).__init__()

        self.table_models = [TreatmentArea()]

    def process(self, locations):
        all_rows = '1=1'
        all_rows = 'GUID = \'{00AEEB90-E846-483E-B677-08821009A066}\''

        for model in self.table_models:
            rows = []
            source = model.source
            fields = model.source_fields()
            destination = model.destination
            destination_fields = model.destination_fields()

            #: query source data for specific table
            print('querying source data')

            arcpy.env.workspace = locations['source']
            with arcpy.da.SearchCursor(in_table=source, field_names=fields, where_clause=all_rows) as cursor:
                #: etl the rows
                print('etling results')
                rows = map(partial(self._etl_row, model), cursor)

            #: write rows to destination table
            print('inserting {} records into destination'.format(len(rows)))

            arcpy.env.workspace = locations['destination']
            with arcpy.da.InsertCursor(in_table=destination, field_names=destination_fields) as cursor:
                for row in rows:
                    row = map(lambda x: x[1], row)
                    cursor.insertRow(row)

    def _etl_row(self, model, row):
        source_data = zip(model.source_fields(), row)

        def etl_row(item):
            field = item[0]
            value = item[1]

            field_info = model.schema[field]

            if 'lookup' in field_info:
                values = Lookup.__dict__[field_info['lookup']]

                if value in values.keys():
                    item = (field, values[value])

            return item

        return map(etl_row, source_data)

        # if table_name == 'crash':
        #     input_keys = Schema.crash_input_keys
        #     etl_keys = Schema.crash_etl_keys
        #     lookup = Schema.crash
        #     formatter = Schema.crash_schema_ordering
        # elif table_name == 'driver':
        #     input_keys = Schema.driver_input_keys
        #     etl_keys = Schema.driver_etl_keys
        #     lookup = Schema.driver
        #     formatter = Schema.driver_schema_ordering
        # elif table_name == 'rollup':
        #     input_keys = Schema.rollup_input_keys
        #     etl_keys = Schema.rollup_etl_keys
        #     lookup = Schema.rollup
        #     formatter = Schema.rollup_schema_ordering
        # else:
        #     raise Exception(file, 'Not a part of the crash, drivers, rollops convention')

        # return self._etl_row_generic(row, lookup, input_keys, etl_keys, formatter)

        return 'hello'

    def _etl_row_generic(self, row, lookup, input_keys, etl_keys, formatter=None):
        # etl_row = dict.fromkeys(etl_keys)

        # for key in row.keys():
        #     if key not in input_keys:
        #         continue

        #     etl_info = lookup[key]

        #     value = row[key]
        #     etl_value = Caster.cast(value, etl_info['type'])

        #     if 'lookup' in etl_info.keys():
        #         lookup_name = etl_info['lookup']
        #         values = Lookup.__dict__[lookup_name]

        #         if etl_value in values.keys():
        #             etl_value = values[etl_value]

        #     etl_row[etl_info['map']] = etl_value

        # if formatter:
        #     return formatter(etl_row)

        # return etl_row

        pass
