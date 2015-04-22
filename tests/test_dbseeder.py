#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
dbseeder
----------------------------------
test the dbseeder module
'''

import unittest
from dbseeder.dbseeder import Seeder
import dbseeder.models as model
from mock import Mock
from os.path import isfile


class TestDbSeeder(unittest.TestCase):

    def setUp(self):
        self.locations = {
            'source': 'connections\WRI on (local).sde',
            'destination': 'connections\WRI_Spatial on (local).sde'
        }

        self.patient = Seeder(self.locations)

    def test_ensure_absolute_path(self):
        self.assertTrue(isfile(self.patient.locations['source']))
        self.assertTrue(isfile(self.patient.locations['destination']))

    def test_ensure_throws_if_not_found(self):
        self.assertRaises(Exception, Seeder, {
            'source': 'not a file'
        })

    def test_get_where_clause_int(self):
        cursor = Mock()
        cursor.execute = Mock(return_value=['\'2\''])

        arcpy = Mock()
        arcpy.ArcSDESQLExecute = Mock(return_value=cursor)

        actual = self.patient._get_where_clause(arcpy, {})
        expected = 'Project_FK in (\'2\')'

        self.assertEqual(actual, expected)

    def test_get_where_clause_array(self):
        cursor = Mock()
        cursor.execute = Mock(return_value=[['\'2\''], ['\'1\'']])

        arcpy = Mock()
        arcpy.ArcSDESQLExecute = Mock(return_value=cursor)

        actual = self.patient._get_where_clause(arcpy, {})
        expected = 'Project_FK in (\'2\',\'1\')'

        self.assertEqual(actual, expected)

    def test_get_where_clause_empty(self):
        cursor = Mock()
        cursor.execute = Mock(return_value=None)

        arcpy = Mock()
        arcpy.ArcSDESQLExecute = Mock(return_value=cursor)

        actual = self.patient._get_where_clause(arcpy, {})

        self.assertIsNone(actual)

    def test_points_etl(self):
        patient = model.Points()
        type = 1
        status = 2
        row = ('shape', 'guid', 'Project_FK', type, type, '   description   ', status, status)
        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', 'Trough'),
                    ('TypeCode', 10),
                    ('Description', 'description'),
                    ('StatusDescription', 'Project'),
                    ('StatusCode', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_points_etl(self):
        patient = model.Points(final=True)
        type = 1
        status = 3
        row = ('shape', 'guid', 'Project_FK', type, type, '   description   ', status, status)
        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', 'Trough'),
                    ('TypeCode', 10),
                    ('Description', 'description'),
                    ('StatusDescription', 'Complete'),
                    ('StatusCode', 3)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_guzzler_etl(self):
        patient = model.Guzzler()
        type = 1
        action = 5
        status = 2
        row = ('shape', 'guid', 'Project_FK', type, action, status, status)
        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', 'Guzzler'),
                    ('TypeCode', 9),
                    ('SubType', 'Big Game'),
                    ('Action', 'Removal'),
                    ('StatusDescription', 'Project'),
                    ('StatusCode', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_guzzler_etl(self):
        patient = model.Guzzler(final=True)
        type = 1
        action = 5
        status = 3
        row = ('shape', 'guid', 'Project_FK', type, action, status, status)
        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', 'Guzzler'),
                    ('TypeCode', 9),
                    ('SubType', 'Big Game'),
                    ('Action', 'Removal'),
                    ('StatusDescription', 'Complete'),
                    ('StatusCode', 3)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_fence_etl(self):
        patient = model.Fence()
        type = (8, 'Fence')
        sub_type = 'Pole top'
        action = 'Reconstruction'
        status = (2, 'Project')

        row = ('shape',
               'guid',
               'Project_FK',
               sub_type,
               action,
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('SubType', sub_type),
                    ('Action', action),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_fence_etl(self):
        patient = model.Fence(final=True)
        type = (8, 'Fence')
        sub_type = 'Pole top'
        action = 'Reconstruction'
        status = (3, 'Complete')

        row = ('shape',
               'guid',
               'Project_FK',
               sub_type,
               action,
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('SubType', sub_type),
                    ('Action', action),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_pipeline_etl(self):
        patient = model.Pipeline()
        type = (7, 'Pipeline')
        sub_type = 'Above surface'
        action = 'Reconstruction'
        status = (2, 'Project')

        row = ('shape',
               'guid',
               'Project_FK',
               sub_type,
               action,
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('SubType', sub_type),
                    ('Action', action),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_pipeline_etl(self):
        patient = model.Pipeline(final=True)
        type = (7, 'Pipeline')
        sub_type = 'Above surface'
        action = 'Reconstruction'
        status = (3, 'Complete')

        row = ('shape',
               'guid',
               'Project_FK',
               sub_type,
               action,
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('SubType', sub_type),
                    ('Action', action),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_dam_etl(self):
        patient = model.Dam()
        type = (6, 'Dam')
        action = 'Reconstruction'
        status = (2, 'Project')

        row = ('shape',
               'guid',
               'Project_FK',
               action,
               status[0],
               status[0])

        expected = [('SHAPE@', 'poly_to_line'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('Action', action),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        self.patient.polygon_to_line = Mock(return_value='poly_to_line')
        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)
        self.patient.polygon_to_line.assert_called_with('shape')

    def test_final_dam_etl(self):
        patient = model.Dam(final=True)
        type = (6, 'Dam')
        action = 'Reconstruction'
        status = (3, 'Complete')
        self.patient.polygon_to_line = Mock(return_value='poly_to_line')

        row = ('shape',
               'guid',
               'Project_FK',
               action,
               status[0],
               status[0])

        expected = [('SHAPE@', 'poly_to_line'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('Action', action),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)
        self.patient.polygon_to_line.assert_called_with('shape')

    def test_affectedarea_etl(self):
        patient = model.AffectedArea()
        type = (5, 'Affected Area')
        status = (2, 'Project')

        row = ('shape',
               'guid',
               'Project_FK',
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_affectedarea_etl(self):
        patient = model.AffectedArea(final=True)
        type = (5, 'Affected Area')
        status = (3, 'Complete')

        row = ('shape',
               'guid',
               'Project_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_easement_etl(self):
        patient = model.EasementAquisition()
        type = (3, 'Easement/Aquisition')
        status = (2, 'Project')

        row = ('shape',
               'guid',
               'Project_FK',
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_easement_etl(self):
        patient = model.EasementAquisition(final=True)
        type = (3, 'Easement/Aquisition')
        status = (3, 'Complete')

        row = ('shape',
               'guid',
               'Project_FK',
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_aquatic_etl(self):
        patient = model.AquaticTreatmentArea()
        type = 'Aquatic/Riparian'
        source_type_code = 2
        type_code = 1
        status = (2, 'Project')

        row = ('shape',
               'guid',
               'Project_FK',
               source_type_code,
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type),
                    ('TypeCode', type_code),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_aquatic_etl(self):
        patient = model.AquaticTreatmentArea(final=True)
        type = 'Aquatic/Riparian'
        source_type_code = 2
        type_code = 1
        status = (3, 'Complete')

        row = ('shape',
               'guid',
               'Project_FK',
               source_type_code,
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type),
                    ('TypeCode', type_code),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_research_etl(self):
        patient = model.Research()
        type = 'Research'
        type_code = 5
        status = (2, 'Project')

        row = ('shape',
               'guid',
               'Project_FK',
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type),
                    ('TypeCode', type_code),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_research_etl(self):
        patient = model.Research(final=True)
        type = 'Research'
        type_code = 5
        status = (3, 'Complete')

        row = ('shape',
               'guid',
               'Project_FK',
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type),
                    ('TypeCode', type_code),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_fishpassage_etl(self):
        patient = model.FishPassage()
        type = 'Fish Passage Structure'
        type_code = 2
        status = (2, 'Project')

        class TestDummy(object):
            pass

        poly = TestDummy()
        poly.centroid = 'centroid'

        row = (poly,
               'guid',
               'Project_FK',
               status[0],
               status[0])

        expected = [('SHAPE@', 'centroid'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type),
                    ('TypeCode', type_code),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_fishpassage_etl(self):
        patient = model.FishPassage(final=True)
        type = 'Fish Passage Structure'
        type_code = 2
        status = (3, 'Complete')

        class TestDummy(object):
            pass

        poly = TestDummy()
        poly.centroid = 'centroid'

        row = (poly,
               'guid',
               'Project_FK',
               status[0],
               status[0])

        expected = [('SHAPE@', 'centroid'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type),
                    ('TypeCode', type_code),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_terrestrial_etl(self):
        patient = model.TerrestrialTreatmentArea()
        type = 'Terrestrial'
        source_type_code = 1
        type_code = 0
        status = (2, 'Project')

        row = ('shape',
               'guid',
               'Project_FK',
               source_type_code,
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type),
                    ('TypeCode', type_code),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_terrestrial_etl(self):
        patient = model.TerrestrialTreatmentArea(final=True)
        type = 'Terrestrial'
        type_code = 0
        source_type_code = 1
        status = (3, 'Complete')

        row = ('shape',
               'guid',
               'Project_FK',
               source_type_code,
               status[0],
               status[0])

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type),
                    ('TypeCode', type_code),
                    ('StatusDescription', status[1]),
                    ('StatusCode', status[0])]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
