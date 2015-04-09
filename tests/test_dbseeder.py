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

if __name__ == '__main__':
    unittest.main()
