#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''ArcGIS Press
Usage:
  dbseeder seed <source> <destination> <where>
  dbseeder (-h | --help)
Options:
  -h --help     Show this screen.
  <source> a file location to a .sde file. eg: "connections\\WRI on PROD.sde"
  <destination> a file location to a .sde file. eg: "connections\\WRI on DEV.sde"
  <where> the base location of the web api. eg: "http://localhost/wri/" or "https://wrimaps.at.utah.gov/WRI_AT/"
'''

import sys
from dbseeder import Seeder
from docopt import docopt


def main():
    arguments = docopt(__doc__)

    locations = {
        'source': arguments['<source>'],
        'destination': arguments['<destination>']
    }

    seeder = Seeder(locations, arguments['<where>'])

    if arguments['seed']:
        return seeder.process()

if __name__ == '__main__':
    sys.exit(main())
