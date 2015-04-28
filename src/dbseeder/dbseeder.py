#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
dbseeder
----------------------------------
the dbseeder module
'''

import models
import re
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
        status_sql = join(parent_directory, '..\\..\\scripts\\sql\\projects_without_finals.sql')
        dedupe_features = join(parent_directory, '..\\..\\scripts\\sql\\delete_features_with_completes.sql')

        with open(seed_sql, 'r') as f:
            self.seed_sql = f.read()

        with open(status_sql, 'r') as f:
            self.status_sql = f.read()

        with open(dedupe_features, 'r') as f:
            self.dedupe_sql = f.read()

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
        import arcpy

        self.set_geometry_types(arcpy, self.locations['destination'])
        total_start = timeit.default_timer()

        print('Building guid to project number lookup')
        models.Lookup.project_id = self.build_guid_ref_table(arcpy, self.locations)

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

        self.set_geometry_types(arcpy, self.locations['destination'], create=False)

        print('Updating Pending Complete Status')
        self.update_status(arcpy, self.locations)

        print('Removing Duplicate Features')
        self.dedup_features(arcpy, self.locations)

        total_end = timeit.default_timer()

        print('finished in {}'.format(round(total_end - total_start, 2)))

    def update_status(self, arcpy, locations):
        where_clause = self._get_where_clause(arcpy, locations['source'])
        fields = ['StatusDescription', 'StatusCode']

        updated = 0
        arcpy.env.workspace = locations['destination']
        with arcpy.da.UpdateCursor(in_table='POLY',
                                   where_clause=where_clause,
                                   field_names=fields) as poly_cursor:
            for row in poly_cursor:
                row[0] = 'Pending Complete'
                row[1] = 6

                poly_cursor.updateRow(row)
                updated += 1

        with arcpy.da.UpdateCursor(in_table='POINT',
                                   where_clause=where_clause,
                                   field_names=fields) as point_cursor:
            for row in point_cursor:
                row[0] = 'Pending Complete'
                row[1] = 6

                point_cursor.updateRow(row)
                updated += 1

        with arcpy.da.UpdateCursor(in_table='LINE',
                                   where_clause=where_clause,
                                   field_names=fields) as line_cursor:
            for row in line_cursor:
                row[0] = 'Pending Complete'
                row[1] = 6

                line_cursor.updateRow(row)
                updated += 1

        print('Updated {} features'.format(updated))

    def build_guid_ref_table(self, arcpy, locations):
        cursor = arcpy.ArcSDESQLExecute(locations['source'])

        try:
            return dict(cursor.execute('select convert(nvarchar(50), guid), project_id from wriproject'))
        finally:
            del cursor

    def dedup_features(self, arcpy, locations):
        cursor = arcpy.ArcSDESQLExecute(locations['destination'])
        try:
            cursor.execute(self.dedupe_sql)
        finally:
            del cursor

    def _get_where_clause(self, arcpy, db):
        where_clause = 'Project_FK in ({})'
        projects = []

        arcpy.env.workspace = db
        cursor = arcpy.ArcSDESQLExecute(db)

        try:
            projects = cursor.execute(self.status_sql)
        except Exception, e:
            print(e)
            print(e.message)
        finally:
            del cursor

        try:
            if len(projects) == 1:
                return where_clause.format(projects[0])

            #: flatten array
            projects = [item for sublist in projects for item in sublist]
        except TypeError:
            if not projects:
                return None

            return where_clause.format(projects)

        return where_clause.format(','.join(projects))

    def _etl_row(self, model, row):
        #: (<PointGeometry, guid, guid, 3.0, u'windmill', 5)

        source_data = model.merge_data(row)

        def etl_row(item):
            #: (source column, destination column, value)
            source_field = item[0]
            destination_field = item[1]
            value = item[2]

            field_info = model.schema[source_field]

            item = (destination_field, value)

            if 'action' in field_info:
                if field_info['action'] == 'strip' and value:
                    value = value.strip()
                    item = (destination_field, value)
                elif field_info['action'] == 'stripcurly' and value:
                    value = re.sub('[{}]', '', value)
                    item = (destination_field, value)
                else:
                    value = None
                    item = (destination_field, value)

            if 'value' in field_info:
                    value = field_info['value']
                    item = (destination_field, value)

            if 'lookup' in field_info:
                values = models.Lookup.__dict__[field_info['lookup']]

                if value in values.keys():
                    item = (destination_field, values[value])
                else:
                    print('{} not found in {}'.format(value, field_info['lookup']))

            if 'etl' in field_info:
                etl_info = field_info['etl']

                if 'method' not in etl_info:
                    return item

                if etl_info['method'] == 'centroid':
                    item = (destination_field, value.centroid)
                elif etl_info['method'] == 'poly_to_line':
                    line = self.polygon_to_line(value)
                    item = (destination_field, line)

            return item

        row = map(etl_row, source_data)

        return row

    def set_geometry_types(self, arcpy, db, create=True):
        cursor = arcpy.ArcSDESQLExecute(db)

        try:
            if create:
                cursor.execute(self.seed_sql)

                return

            cursor.execute('delete from {} where StatusDescription = \'{}\''.format('POINT', 'temporary'))
            cursor.execute('delete from {} where StatusDescription = \'{}\''.format('LINE', 'temporary'))
            cursor.execute('delete from {} where StatusDescription = \'{}\''.format('POLY', 'temporary'))
        finally:
            del cursor

    def polygon_to_line(self, polygon):
        import arcpy

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
