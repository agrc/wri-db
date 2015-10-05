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
            'source': 'connections\WRI_Source on (local).sde',
            'destination': 'connections\WRI on (local).sde'
        }

        self.patient = Seeder(self.locations)

        model.Lookup.project_id = {
            'Project_FK': 1,
            'CompletedProject_FK': 2
        }

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
        source_type = 1
        type = self.get_type_pair_for('Trough', model.Lookup.other_points)
        type_code = self.get_type_pair_for(type[0], model.Lookup.other_points_code, 0)
        original_project_status = self.get_type_pair_for('Project', model.Lookup.original_status)[0]
        current_project_status = self.get_type_pair_for('Current', model.Lookup.new_status)

        row = ('shape', 'guid', 'Project_FK', source_type, source_type, '   description   ', original_project_status, original_project_status, 'Project_FK')
        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type_code[1]),
                    ('Description', 'description'),
                    ('StatusDescription', current_project_status[1]),
                    ('StatusCode', current_project_status[0]),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_points_etl(self):
        patient = model.Points(final=True)
        source_type = 2
        type = self.get_type_pair_for('Water control structure', model.Lookup.other_points)
        type_code = self.get_type_pair_for(type[0], model.Lookup.other_points_code, 0)
        current_project_status = self.get_type_pair_for('Completed', model.Lookup.new_status)
        row = ('shape', 'guid', 'CompletedProject_FK', source_type, source_type, '   description   ', 'CompletedProject_FK')
        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type_code[1]),
                    ('Description', 'description'),
                    ('StatusDescription', current_project_status[1]),
                    ('StatusCode', current_project_status[0]),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_guzzler_etl(self):
        patient = model.Guzzler()
        type = self.get_feature_type_pair('Guzzler')
        action = 5
        original_project_status = 2
        new_project_status = 3
        row = ('shape', 'guid', 'Project_FK', 1, action, original_project_status, original_project_status, 'Project_FK')
        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('FeatureSubTypeDescription', 'Big Game'),
                    ('ActionDescription', 'Removal'),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', new_project_status),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_guzzler_etl(self):
        patient = model.Guzzler(final=True)
        type = self.get_feature_type_pair('Guzzler')
        action = 5
        row = ('shape', 'guid', 'CompletedProject_FK', 1, action, 'CompletedProject_FK')
        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('FeatureSubTypeDescription', 'Big Game'),
                    ('ActionDescription', 'Removal'),
                    ('StatusDescription', 'Completed'),
                    ('StatusCode', 5),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_fence_etl(self):
        patient = model.Fence()
        type = self.get_feature_type_pair('Fence')
        sub_type = 'Pole top'
        action = 'Reconstruction'
        original_project_status = 2
        new_project_status = 3
        row = ('shape',
               'guid',
               'Project_FK',
               sub_type,
               action,
               original_project_status,
               original_project_status,
               'Project_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('FeatureSubTypeDescription', sub_type),
                    ('ActionDescription', action),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', new_project_status),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_real_fence(self):
        patient = model.Fence()

        row = (495,  #: shape
               '1E383419-8A37-4454-98EA-2E23E2DD6D30',  #: guid
               'Project_FK',  #: pfk
               2,  #: fence type
               3,  #: fence action
               2,  #: status
               2,  #: status
               'Project_FK')  #: pfk
        expected = ([
                    ('SHAPE@', 495),  #: shape
                    ('GUID', '1E383419-8A37-4454-98EA-2E23E2DD6D30'),  #: guid
                    ('Project_FK', 'Project_FK'),  #: pfk
                    ('TypeDescription', 'Fence'),
                    ('TypeCode', 10),
                    ('FeatureSubTypeDescription', 'Buck pole'),
                    ('ActionDescription', 'Construction'),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', 3),
                    ('Project_Id', 1)])

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_fence_etl(self):
        patient = model.Fence(final=True)
        type = self.get_feature_type_pair('Fence')
        sub_type = 'Pole top'
        action = 'Reconstruction'

        row = ('shape',
               'guid',
               'CompletedProject_FK',
               sub_type,
               action,
               'CompletedProject_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('FeatureSubTypeDescription', sub_type),
                    ('ActionDescription', action),
                    ('StatusDescription', 'Completed'),
                    ('StatusCode', 5),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_pipeline_etl(self):
        patient = model.Pipeline()
        type = self.get_feature_type_pair('Pipeline')
        sub_type = 'Above surface'
        action = 'Reconstruction'
        original_project_status = 2
        new_project_status = 3

        row = ('shape',
               'guid',
               'Project_FK',
               sub_type,
               action,
               original_project_status,
               original_project_status,
               'Project_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('FeatureSubTypeDescription', sub_type),
                    ('ActionDescription', action),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', new_project_status),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_pipeline_etl(self):
        patient = model.Pipeline(final=True)
        type = self.get_feature_type_pair('Pipeline')
        sub_type = 'Above surface'
        action = 'Reconstruction'

        row = ('shape',
               'guid',
               'CompletedProject_FK',
               sub_type,
               action,
               'CompletedProject_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('FeatureSubTypeDescription', sub_type),
                    ('ActionDescription', action),
                    ('StatusDescription', 'Completed'),
                    ('StatusCode', 5),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_dam_etl(self):
        patient = model.Dam()
        type = self.get_feature_type_pair('Dam')
        action = 'Reconstruction'
        original_project_status = 2
        current_project_status = 3

        row = ('shape',
               'guid',
               'Project_FK',
               action,
               original_project_status,
               original_project_status,
               'Project_FK')

        expected = [('SHAPE@', 'poly_to_line'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('ActionDescription', action),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', current_project_status),
                    ('Project_Id', 1)]

        self.patient.polygon_to_line = Mock(return_value='poly_to_line')
        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)
        self.patient.polygon_to_line.assert_called_with('shape')

    def test_final_dam_etl(self):
        patient = model.Dam(final=True)
        type = self.get_feature_type_pair('Dam')
        action = 'Reconstruction'
        self.patient.polygon_to_line = Mock(return_value='poly_to_line')

        row = ('shape',
               'guid',
               'CompletedProject_FK',
               action,
               'CompletedProject_FK')

        expected = [('SHAPE@', 'poly_to_line'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('ActionDescription', action),
                    ('StatusDescription', 'Completed'),
                    ('StatusCode', 5),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)
        self.patient.polygon_to_line.assert_called_with('shape')

    def test_affectedarea_etl(self):
        patient = model.AffectedArea()
        type = self.get_feature_type_pair('Affected Area')
        original_project_status = 2
        current_project_status = 3

        row = ('shape',
               'guid',
               'Project_FK',
               original_project_status,
               original_project_status,
               'Project_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', current_project_status),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_affectedarea_etl(self):
        patient = model.AffectedArea(final=True)
        type = self.get_feature_type_pair('Affected Area')

        row = ('shape',
               'guid',
               'CompletedProject_FK',
               'CompletedProject_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Completed'),
                    ('StatusCode', 5),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_easement_etl(self):
        patient = model.EasementAquisition()
        type = self.get_feature_type_pair('Easement/Acquisition')
        original_project_status = 2
        current_project_status = 3

        row = ('shape',
               'guid',
               'Project_FK',
               original_project_status,
               original_project_status,
               'Project_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', current_project_status),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_easement_etl(self):
        patient = model.EasementAquisition(final=True)
        type = self.get_feature_type_pair('Easement/Acquisition')
        current_project_status = self.get_type_pair_for('Completed', model.Lookup.new_status)

        row = ('shape',
               'guid',
               'CompletedProject_FK',
               'CompletedProject_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', current_project_status[1]),
                    ('StatusCode', current_project_status[0]),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_aquatic_etl(self):
        patient = model.AquaticTreatmentArea()
        type = self.get_feature_type_pair('Aquatic/Riparian Treatment Area')
        source_type_code = 2
        original_project_status = self.get_type_pair_for('Project', model.Lookup.original_status)[0]
        current_project_status = self.get_type_pair_for('Current', model.Lookup.new_status)

        row = ('shape',
               'guid',
               'Project_FK',
               source_type_code,
               original_project_status,
               original_project_status,
               'Project_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', current_project_status[1]),
                    ('StatusCode', current_project_status[0]),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_aquatic_etl(self):
        patient = model.AquaticTreatmentArea(final=True)
        type = self.get_feature_type_pair('Aquatic/Riparian Treatment Area')
        source_type_code = 2

        row = ('shape',
               'guid',
               'CompletedProject_FK',
               source_type_code,
               'CompletedProject_FK',)

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Completed'),
                    ('StatusCode', 5),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_research_etl(self):
        patient = model.Research()
        type = self.get_feature_type_pair('Affected Area')
        original_project_status = 2
        new_project_status = 3

        row = ('shape',
               'guid',
               'Project_FK',
               original_project_status,
               original_project_status,
               'Project_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', new_project_status),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_research_etl(self):
        patient = model.Research(final=True)
        type = self.get_feature_type_pair('Affected Area')

        row = ('shape',
               'guid',
               'CompletedProject_FK',
               'CompletedProject_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Completed'),
                    ('StatusCode', 5),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_fishpassage_etl(self):
        patient = model.FishPassage()
        type = self.get_feature_type_pair('Fish passage structure')
        original_project_status = 2
        new_project_status = 3

        class TestDummy(object):
            pass

        poly = TestDummy()
        poly.centroid = 'centroid'

        row = (poly,
               'guid',
               'Project_FK',
               original_project_status,
               original_project_status,
               'Project_FK')

        expected = [('SHAPE@', 'centroid'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', new_project_status),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_fishpassage_etl(self):
        patient = model.FishPassage(final=True)
        type = self.get_feature_type_pair('Fish passage structure')

        class TestDummy(object):
            pass

        poly = TestDummy()
        poly.centroid = 'centroid'

        row = (poly,
               'guid',
               'CompletedProject_FK',
               'CompletedProject_FK')

        expected = [('SHAPE@', 'centroid'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Completed'),
                    ('StatusCode', 5),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_terrestrial_etl(self):
        patient = model.TerrestrialTreatmentArea()
        type = self.get_feature_type_pair('Terrestrial Treatment Area')
        source_type_code = 1
        project_status = 2

        row = ('shape',
               'guid',
               'Project_FK',
               source_type_code,
               project_status,
               project_status,
               'Project_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'Project_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Current'),
                    ('StatusCode', 3),
                    ('Project_Id', 1)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def test_final_terrestrial_etl(self):
        patient = model.TerrestrialTreatmentArea(final=True)
        type = self.get_feature_type_pair('Terrestrial Treatment Area')
        source_type_code = 1

        row = ('shape',
               'guid',
               'CompletedProject_FK',
               source_type_code,
               'CompletedProject_FK')

        expected = [('SHAPE@', 'shape'),
                    ('GUID', 'guid'),
                    ('Project_FK', 'CompletedProject_FK'),
                    ('TypeDescription', type[1]),
                    ('TypeCode', type[0]),
                    ('StatusDescription', 'Completed'),
                    ('StatusCode', 5),
                    ('Project_Id', 2)]

        actual = self.patient._etl_row(patient, row)

        self.assertEqual(actual, expected)

    def get_feature_type_pair(self, type):
        for pair in model.Lookup.feature_type.iteritems():
            if pair[1] == type:
                return pair

    def get_type_pair_for(self, type, lookup, index=1):
        for pair in lookup.iteritems():
            if pair[index] == type:
                return pair

if __name__ == '__main__':
    unittest.main()
