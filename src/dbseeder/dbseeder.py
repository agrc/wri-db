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
import requests
from functools import partial
from models import Lookup
from os.path import join, dirname, isfile


class Seeder(object):

    def __init__(self, locations, where):
        super(Seeder, self).__init__()

        self.Lookup = Lookup()

        self.api_url_template = where + 'api/historical/project/{}/create-related-data'

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
        truncate_features = join(parent_directory, '..\\..\\scripts\\sql\\truncate_spatial_tables.sql')

        with open(seed_sql, 'r') as f:
            self.seed_sql = f.read()

        with open(status_sql, 'r') as f:
            self.status_sql = f.read()

        with open(dedupe_features, 'r') as f:
            self.dedupe_sql = f.read()

        with open(truncate_features, 'r') as f:
            self.truncate_sql = f.read()

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

        total_start = timeit.default_timer()
        self.web_mercator = arcpy.SpatialReference(3857)

        print('Truncating spatial table features')
        cursor = arcpy.ArcSDESQLExecute(self.locations['destination'])
        try:
            cursor.execute(self.truncate_sql)
        finally:
            del cursor

        print('Seeding table geometry types')
        self.set_geometry_types(arcpy, self.locations['destination'])

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
                                       where_clause=model.where_clause,
                                       spatial_reference=self.web_mercator) as cursor:
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

        print('Updating Related Tables and Project Centroids')
        self.update_related_and_centroids(arcpy, self.locations)

        total_end = timeit.default_timer()

        print('finished in {}'.format(round(total_end - total_start, 2)))

    def update_status(self, arcpy, locations):
        where_clause = self._get_where_clause(arcpy, locations['source'])

        codes = None
        for pair in Lookup.new_status.iteritems():
            if pair[1] == 'Pending Completed':
                codes = pair

        cursor = arcpy.ArcSDESQLExecute(locations['destination'])

        cursor.execute('update dbo.Poly ' +
                       'set StatusDescription = \'{}\', '.format(codes[1]) +
                       'StatusCode = {} where {}'.format(codes[0], where_clause))

        cursor.execute('update dbo.Point ' +
                       'set StatusDescription = \'{}\', '.format(codes[1]) +
                       'StatusCode = {} where {}'.format(codes[0], where_clause))

        cursor.execute('update dbo.Line ' +
                       'set StatusDescription = \'{}\', '.format(codes[1]) +
                       'StatusCode = {} where {}'.format(codes[0], where_clause))

        where_clause = where_clause.replace('Project_FK', 'GUID')
        cursor.execute('update dbo.Project ' +
                       'set Status = \'{}\', '.format(codes[1]) +
                       'StatusID = {} where {}'.format(codes[0], where_clause))

        del cursor

        print('Updated features')

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

                operations = etl_info['method']
                if isinstance(operations, basestring):
                    item = self.handle_etl(operations, value, destination_field)
                else:
                    updated = None
                    for operation in operations:
                        if updated is None:
                            updated = self.handle_etl(operation, value, destination_field)
                        else:
                            updated = self.handle_etl(operation, updated, destination_field)

                    item = updated

            return item

        row = map(etl_row, source_data)

        return row

    def set_geometry_types(self, arcpy, db, create=True):
        cursor = arcpy.ArcSDESQLExecute(db)

        try:
            if create:
                cursor.execute(self.seed_sql)

                return

            cursor.execute('delete from {} where StatusDescription = \'{}\''.format('dbo.POINT', 'temporary'))
            cursor.execute('delete from {} where StatusDescription = \'{}\''.format('dbo.LINE', 'temporary'))
            cursor.execute('delete from {} where StatusDescription = \'{}\''.format('dbo.POLY', 'temporary'))
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

    def point_to_multipoint(self, point):
        import arcpy

        return arcpy.Multipoint(arcpy.Array(point))

    def handle_etl(self, operation, value, destination_field):
        if operation == 'centroid':
            item = (destination_field, value.centroid)
        elif operation == 'poly_to_line':
            line = self.polygon_to_line(value)
            item = (destination_field, line)
        elif operation == 'point_to_multipoint':
            if isinstance(value, tuple):
                value = value[1]

            try:
                value = value.getPart(0)
            except:
                pass

            item = (destination_field, self.point_to_multipoint(value))

        return item

    def update_related_and_centroids(self, arcpy, locations):
        cursor = arcpy.ArcSDESQLExecute(locations['destination'])
        project_ids = None

        if self.api_url_template.startswith('https'):
            requests.packages.urllib3.disable_warnings()

        try:
            project_ids = cursor.execute('select project_id from project')
        finally:
            del cursor

        project_ids = [item for iter_ in project_ids for item in iter_]
        project_ids.sort()
        i = 0
        progress = 10
        while project_ids:
            failed_projects = []
            for id in project_ids:
                #: make request to server
                url = self.api_url_template.format(id)
                r = requests.put(url, verify=False)
                i += 1
                if i % progress == 0:
                    print '{} of {}'.format(i, len(project_ids))

                if r.status_code != 204:
                    failed_projects.append(id)
                    print url, r.status_code

            print('acting on {} failed ids'.format(len(failed_projects)))
            project_ids = failed_projects
            progress = 1
            i = 0
