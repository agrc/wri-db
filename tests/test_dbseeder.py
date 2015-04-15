#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
dbseeder
----------------------------------
test the dbseeder module
'''

import unittest
from dbseeder.dbseeder import Seeder
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

    def test_format_esri_guid(self):
        actual = self.patient.format_esri_guid('123')
        expected = '\'{123}\''

        self.assertEqual(actual, expected)

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

if __name__ == '__main__':
    unittest.main()
