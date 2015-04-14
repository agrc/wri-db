#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
dbseeder
----------------------------------
the dbseeder module
'''

import arcpy
import models
import timeit
from functools import partial
from models import Lookup
from os.path import join, dirname, isfile


class Seeder(object):

    def __init__(self, locations):
        super(Seeder, self).__init__()

        self.Lookup = Lookup()

        self.table_models = [
            models.Points(),
            models.Points(final=True),
            models.Guzzler(),
            models.Guzzler(final=True),
            models.Fence(),
            models.Fence(final=True),
            models.Pipeline(),
            models.Pipeline(final=True),
            models.Dam(),
            models.Dam(final=True),
            models.AffectedArea(),
            models.AffectedArea(final=True),
            models.Research(),
            models.Research(final=True),
            models.FishPassage(),
            models.FishPassage(final=True),
            models.EasementAquisition(),
            models.EasementAquisition(final=True),
            models.AquaticTreatmentArea(),
            models.AquaticTreatmentArea(final=True),
            models.TerrestrialTreatmentArea(),
            models.TerrestrialTreatmentArea(final=True),
        ]

        self.scratch_line = '%scratchGDB%\\wri_dbseeder_line'

        parent_directory = dirname(__file__)
        seed_sql = join(parent_directory, '..\\..\\scripts\\sql\\seed_feature_types.sql')

        with open(seed_sql, 'r') as f:
            self.seed_sql = f.read()

        def ensure_absolute_path(file):
            if not isfile(file):
                file = join(parent_directory, file)
                if not isfile(file):
                    raise Exception('database connection file not found')

            return file

        self.locations = locations

        for key in locations.keys():
            self.locations[key] = ensure_absolute_path(locations[key])

    def process(self):
        self.set_geometry_types(self.locations['destination'])
        total_start = timeit.default_timer()

        for model in self.table_models:
            print(model.name)
            start = timeit.default_timer()

            rows = []
            source_table = model.source
            source_fields = model.source_fields()
            destination_table = model.destination
            destination_fields = model.destination_fields()

            #: query source data for specific table
            print('- querying source data')

            arcpy.env.workspace = self.locations['source']
            with arcpy.da.SearchCursor(in_table=source_table,
                                       field_names=source_fields,
                                       where_clause=model.where_clause) as cursor:
                #: etl the rows
                print('- etling results')
                rows = map(partial(self._etl_row, model), cursor)

            arcpy.env.workspace = self.locations['destination']

            #: write rows to destination table
            print('- inserting {} records into destination: {}'.format(len(rows), destination_table))
            with arcpy.da.InsertCursor(in_table=destination_table,
                                       field_names=destination_fields) as cursor:
                for row in rows:
                    row = map(lambda x: x[1], row)
                    try:
                        cursor.insertRow(row)
                    except Exception, e:
                        print destination_fields
                        print row
                        end = timeit.default_timer()
                        print('- {} seconds'.format(round(end-start, 2)))
                        raise e

            end = timeit.default_timer()
            print('- {} seconds'.format(round(end-start, 2)))

        self.set_geometry_types(self.locations['destination'], create=False)

        total_end = timeit.default_timer()

        print('finished in {}'.format(round(total_end - total_start, 2)))

    def _etl_row(self, model, row):
        #: (<PointGeometry, guid, guid, 3.0, u'windmill', 5)

        source_data = zip(model.source_fields(), row)
        unmapped_fields = model.unmapped_fields()
        etl_fields = model.etl_fields()

        def etl_row(item):
            field = item[0]
            value = item[1]

            field_info = model.schema[field]

            if 'lookup' in field_info:
                values = models.Lookup.__dict__[field_info['lookup']]
                if value in values.keys():
                    item = (field, values[value])

            if 'action' in field_info:
                if field_info['action'] == 'strip' and value:
                    item = (field, value.strip())
                else:
                    item = (field, None)

            return item

        row = map(etl_row, source_data)

        if unmapped_fields:
            #: (6, '*Status')
            for field in unmapped_fields:
                field_info = model.schema[field[1]]

                if 'value' in field_info:
                    item = field_info['value']
                    row.insert(field[0], (field_info['map'], item))

        if etl_fields:
            #: (0, {'out': 'POINT', 'method': 'centroid', 'in': 'POLY'})
            for field in etl_fields:
                index = field[0]
                etl_info = field[1]

                attribute_name = row[index][0]
                attribute_value = row[index][1]

                if 'method' not in etl_info:
                    continue

                if etl_info['method'] == 'centroid':
                    row[index] = (attribute_name, attribute_value.centroid)
                elif etl_info['method'] == 'poly_to_line':
                    line = self.polygon_to_line(attribute_value)
                    row[index] = (attribute_name, line)

        return row

    def set_geometry_types(self, db, create=True):
        cursor = arcpy.ArcSDESQLExecute(db)

        if create:
            cursor.execute(self.seed_sql)

            return

        cursor.execute('delete from {} where status = \'{}\''.format('POINT', 'temporary'))
        cursor.execute('delete from {} where status = \'{}\''.format('LINE', 'temporary'))
        cursor.execute('delete from {} where status = \'{}\''.format('POLY', 'temporary'))

    def polygon_to_line(self, polygon):
        _workspace = arcpy.env.workspace
        arcpy.env.workspace = None

        try:
            arcpy.PolygonToLine_management(polygon, self.scratch_line, 'IGNORE_NEIGHBORS')
            line = None

            with arcpy.da.SearchCursor(self.scratch_line, 'SHAPE@') as cursor:
                line = cursor.next()[0]

            arcpy.Delete_management(self.scratch_line)
        except Exception, e:
            raise e
        finally:
            arcpy.env.workspace = _workspace

        return line

    def filter_rows_by_model(self, rows):
        models = {
            #: {'Status': 'Project', 'SHAPE@': <Polygon>, 'Project_FK': guid, 'GUID': guid, 'Type': 'Aquatic/Riparian'}
            'FishPassage': [],
            'Original': [],
        }

        for row in rows:
            if 'model' not in row.keys():
                models['Original'].append(row)

            type = row['model']
            del row['model']

            models[type].append(row)

        return models
