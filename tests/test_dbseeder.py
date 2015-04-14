#!usr/bin/env python
# -*- coding: utf-8 -*-

'''
dbseeder
----------------------------------
test the dbseeder module
'''

import unittest
from dbseeder.dbseeder import Seeder
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

    def test_destintation_table_filter(self):
        rows = [
            (('data', '.2'), ('table', 'POINT')),
            (('data', '-1'), ('table', 'LINE')),
            (('data', '1'), ('table', 'POLY')),
            (('data', '2'), ('table', 'POLY')),
            (('data', '.1'), ('table', 'POINT')),
            (('data', '3'), ('table', 'POLY'))
        ]

        expected_point = [
            ('data', '.2'),
            ('data', '.1'),
        ]
        expected_line = [
            ('data', '-1')
        ]
        expected_poly = [
            ('data', '1'),
            ('data', '2'),
            ('data', '3'),
        ]

        actual = self.patient.filter_table_rows(rows)

        self.assertEqual(len(actual.keys()), 3)
        self.assertListEqual(actual['POINT'], expected_point)
        self.assertListEqual(actual['LINE'], expected_line)
        self.assertListEqual(actual['POLY'], expected_poly)


if __name__ == '__main__':
    unittest.main()
