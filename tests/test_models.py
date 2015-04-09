#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
services
----------------------------------
test the models module
'''

import unittest
import dbseeder.models as model


class TestGuzzler(unittest.TestCase):

    def setUp(self):
        self.patient = model.Guzzler()

    def test_destination_fields(self):
        actual = self.patient.destination_fields()
        expected = [
            'SHAPE@',
            'GUID',
            'Project_FK',
            'Type',
            'SubType',
            'Action',
            'Completed',
            'Status',
        ]

        self.assertListEqual(actual, expected)

    def test_destination_fields_for_incomplete(self):
        self.patient.incomplete = True

        actual = self.patient.destination_fields()
        expected = [
            'GUID',
            'Project_FK',
            'Type',
            'SubType',
            'Action',
            'Completed',
        ]

        self.assertListEqual(actual, expected)

    def test_source_fields(self):
        actual = self.patient.source_fields()
        expected = [
            'SHAPE@',
            'GUID',
            'Project_FK',
            'GuzzlerType',
            'GuzzlerAction',
            'Completed',
            'Status',
        ]

        self.assertListEqual(actual, expected)

    def test_source_fields_for_incomplete(self):
        self.patient.incomplete = True

        actual = self.patient.source_fields()
        expected = [
            'GUID',
            'Project_FK',
            'GuzzlerType',
            'GuzzlerAction',
            'Completed',
        ]

        self.assertListEqual(actual, expected)

    def test_unmapped_fields(self):
        actual = self.patient.unmapped_fields()
        expected = [('*Type', 3)]

        self.assertListEqual(actual, expected)

    def test_unmapped_fields_for_incomplete(self):
        #: index needs to drop since shape is first 0 index
        self.patient.incomplete = True

        actual = self.patient.unmapped_fields()
        expected = [('*Type', 2)]

        self.assertListEqual(actual, expected)

    def test_etl_fields(self):
        self.patient.schema['ETL'] = {
            'type': 'shape',
            'map': 'SHAPE@',
            'etl': {
                'geometry': {
                    'in': 'POINT',
                    'out': 'MULTIPOINT'
                }
            },
            'order': 6
        }

        actual = self.patient.etl_fields()
        expected = [(6, {
            'geometry': {
                    'in': 'POINT',
                    'out': 'MULTIPOINT'
                    }
        })]

        self.assertListEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
