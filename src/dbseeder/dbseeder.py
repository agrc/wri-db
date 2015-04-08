#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
dbseeder
----------------------------------
the dbseeder module
'''

import arcpy
from functools import partial
from os.path import join, dirname
import models


class Seeder(object):

    def __init__(self):
        super(Seeder, self).__init__()

        self.table_models = [
            models.Dam(),
            models.Guzzler(),
            models.Points(),
            models.Fence(),
            models.Pipeline(),
            models.AffectedArea(),
            models.TreatmentArea(),
        ]

        dir = dirname(__file__)
        filename = join(dir, '..\\..\\scripts\\sql\\seed_feature_types.sql')

        with open(filename, 'r') as f:
            self.seed_sql = f.read()

    def process(self, locations):
        all_rows = '1=1'
        # all_rows = 'GUID = \'{00AEEB90-E846-483E-B677-08821009A066}\''

        self.set_geometry_types(locations['destination'])

        for model in self.table_models:
            rows = []
            source = model.source

            fields = model.source_fields()
            destination = model.destination
            destination_fields = model.destination_fields()

            #: query source data for specific table
            print('querying source data: {}'.format(model.source))

            arcpy.env.workspace = locations['source']
            with arcpy.da.SearchCursor(in_table=source,
                                       field_names=fields,
                                       where_clause=all_rows) as cursor:
                #: etl the rows
                print('etling results')
                rows = map(partial(self._etl_row, model), cursor)

            #: write rows to destination table
            print('inserting {} records into destination: {}'.format(len(rows), model.destination))

            arcpy.env.workspace = locations['destination']

            with arcpy.da.InsertCursor(in_table=destination,
                                       field_names=destination_fields) as cursor:
                for row in rows:
                    row = map(lambda x: x[1], row)
                    try:
                        cursor.insertRow(row)
                    except Exception, e:
                        print destination_fields
                        print row
                        raise e

        self.set_geometry_types(locations['destination'], create=False)

    def _etl_row(self, model, row):
        source_data = zip(model.source_fields(), row)
        unmapped_fields = model.unmapped_fields()
        # etl_fields = model.etl_fields()

        def etl_row(item):
            field = item[0]
            value = item[1]

            field_info = model.schema[field]

            if 'lookup' in field_info:
                values = models.Lookup.__dict__[field_info['lookup']]
                if value in values.keys():
                    item = (field, values[value])

            return item

        row = map(etl_row, source_data)

        if unmapped_fields:
            for field in unmapped_fields:
                field_info = model.schema[field[0]]

                if 'value' in field_info:
                    item = field_info['value']
                    row.insert(field[1], (field_info['map'], item))

        return row

    def set_geometry_types(self, db, create=True):
        cursor = arcpy.ArcSDESQLExecute(db)

        if create:
            cursor.execute(self.seed_sql)

            return

        cursor.execute('delete from {} where status = \'{}\''.format('POINT', 'temporary'))
        cursor.execute('delete from {} where status = \'{}\''.format('LINE', 'temporary'))
        cursor.execute('delete from {} where status = \'{}\''.format('POLY', 'temporary'))
