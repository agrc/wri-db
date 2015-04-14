#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
services
----------------------------------
test the models module
'''

import unittest
import dbseeder.models as model
from mock import Mock


class TestTable(unittest.TestCase):

    def setUp(self):
        self.patient = model.Table()
        self.schemas = [
            'base_schema',
            'final_schema',
        ]
        self.schema = [{
            'SHAPE@': {
                'type': 'shape',
                'map': 'MAPPED-SHAPE@',
                'order': 0,
                'etl': {
                    'in': 'POLY',
                    'out': 'LINE',
                    'method': 'poly_to_line'
                }
            },
            '*Type': {
                'type': 'string',
                'map': 'MAPPED-Type',
                'value': 'Guzzler',
                'order': 1
            },
            'Status': {
                'type': 'string',
                'map': 'MAPPED-Status',
                'lookup': 'status',
                'order': 2
            }
        }, {
            'SHAPE@': {
                'type': 'shape',
                'map': 'MAPPED-SHAPE@',
                'order': 0
            },
            '*Type': {
                'type': 'string',
                'map': 'MAPPED-Type',
                'value': 'Guzzler',
                'order': 1
            },
            'Completed': {
                'type': 'string',
                'map': 'MAPPED-Completed',
                'order': 2
            },
            '*Status': {
                'type': 'string',
                'map': 'MAPPED-Status',
                'value': 'Complete',
                'order': 3
            }
        }]

        self.patient.set_schema(False, self.schema)

    def test_format_source_table(self):
        is_final = False

        actual = self.patient.format_source_table('{}{}', ['owner', is_final])
        expected = 'owner'

        self.assertEqual(actual, expected)

    def test_format_source_table_final(self):
        is_final = True

        actual = self.patient.format_source_table('{}{}', ['owner', is_final])
        expected = 'ownerFINAL'

        self.assertEqual(actual, expected)

    def test_set_schema(self):
        is_final = False

        actual = self.patient.set_schema(is_final, self.schemas)

        expected = 'base_schema'

        self.assertEqual(actual, expected)

    def test_set_schema_final(self):
        is_final = True

        actual = self.patient.set_schema(is_final, self.schemas)

        expected = 'final_schema'

        self.assertEqual(actual, expected)

    def test_destination_fields(self):
        is_final = False

        self.patient.set_schema(is_final, self.schema)

        actual = self.patient.destination_fields()
        expected = [
            'MAPPED-SHAPE@',
            'MAPPED-Type',
            'MAPPED-Status',
        ]

        self.assertListEqual(actual, expected)

    def test_destination_fields_final(self):
        is_final = True

        self.patient.set_schema(is_final, self.schema)

        actual = self.patient.destination_fields()
        expected = [
            'MAPPED-SHAPE@',
            'MAPPED-Type',
            'MAPPED-Completed',
            'MAPPED-Status',
        ]

        self.assertListEqual(actual, expected)

    def test_source_fields(self):
        is_final = False

        self.patient.set_schema(is_final, self.schema)

        actual = self.patient.source_fields()
        expected = [
            'SHAPE@',
            'Status',
        ]

        self.assertListEqual(actual, expected)

    def test_source_fields_final(self):
        is_final = True

        self.patient.set_schema(is_final, self.schema)

        actual = self.patient.source_fields()
        expected = [
            'SHAPE@',
            'Completed',
        ]

        self.assertListEqual(actual, expected)

    def test_unmapped_fields(self):
        is_final = False

        self.patient.set_schema(is_final, self.schema)

        actual = self.patient.unmapped_fields()
        expected = [(1, '*Type')]

        self.assertListEqual(actual, expected)

    def test_unmapped_fields_final(self):
        is_final = True

        self.patient.set_schema(is_final, self.schema)

        actual = self.patient.unmapped_fields()
        expected = [(1, '*Type'), (3, '*Status')]

        self.assertListEqual(actual, expected)

    def test_etl_fields(self):
        actual = self.patient.etl_fields()
        expected = [(0, {
                    'in': 'POLY',
                    'out': 'LINE',
                    'method': 'poly_to_line'
                    })]

        self.assertListEqual(actual, expected)

    def test_etl_fields_final(self):
        is_final = True

        self.patient.set_schema(is_final, self.schema)

        actual = self.patient.etl_fields()
        expected = []

        self.assertListEqual(actual, expected)


class TreatmentArea(unittest.TestCase):

    def setUp(self):
        self.patient = model.TreatmentArea()
        self.schemas = [
            'base_schema',
            'final_schema',
        ]
        self.schema = [{
            'SHAPE@': {
                'type': 'shape',
                'map': 'MAPPED-SHAPE@',
                'order': 0,
                'etl': {
                    'in': 'POLY',
                    'out': 'LINE',
                    'method': 'poly_to_line'
                }
            },
            '*Type': {
                'type': 'string',
                'map': 'MAPPED-Type',
                'value': 'Guzzler',
                'order': 1
            },
            'Status': {
                'type': 'string',
                'map': 'MAPPED-Status',
                'lookup': 'status',
                'order': 2
            }
        }, {
            'SHAPE@': {
                'type': 'shape',
                'map': 'MAPPED-SHAPE@',
                'order': 0
            },
            '*Type': {
                'type': 'string',
                'map': 'MAPPED-Type',
                'value': 'Guzzler',
                'order': 1
            },
            'Completed': {
                'type': 'string',
                'map': 'MAPPED-Completed',
                'order': 2
            },
            '*Status': {
                'type': 'string',
                'map': 'MAPPED-Status',
                'value': 'Complete',
                'order': 3
            }
        }]

        self.patient.set_schema(False, self.schema)

    def test_check_actions(self):
        sql = 'select ActionCode from WRIAQUATICRIPARIANACTION where treatmentarea_fk = \'guid\''

        cursor = Mock()
        cursor.execute = Mock(return_value=1)

        arcpy = Mock()
        arcpy.ArcSDESQLExecute = Mock(return_value=cursor)

        self.patient.check_actions(arcpy, 'db', {'Type': 'Aquatic/Riparian', 'GUID': 'guid'})

        cursor.execute.assert_called_with(sql)
        arcpy.ArcSDESQLExecute.assert_called_with('db')

    def test_format_guid(self):
        actual = self.patient.format_guid('{123}')
        expected = '123'

        self.assertEqual(actual, expected)

    def test_has_fish_when_code_is_1(self):
        actual = self.patient.has_fish(1)

        self.assertTrue(actual)

    def test_has_fish_when_code_is_not_1(self):
        actual = self.patient.has_fish(0)

        self.assertFalse(actual)

    def test_has_fish_when_code_has_1(self):
        actual = self.patient.has_fish([0, 3, 1])

        self.assertTrue(actual)

    def test_has_fish_when_1_not_in(self):
        actual = self.patient.has_fish([0, 2, 3, 4])

        self.assertFalse(actual)

    def test_update_row_for_fish_with_true(self):
        row = {}
        actions = 1

        actual = self.patient.update_row_for_fish(actions, row)
        expected = {'table': 'POINT'}

        self.assertEqual(actual, expected)

    def test_update_row_for_fish_with_false(self):
        row = {}
        actions = [0, 2, 3]

        actual = self.patient.update_row_for_fish(actions, row)
        expected = {}

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
