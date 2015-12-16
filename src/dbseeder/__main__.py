#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''WRI Database Conversion tool
Usage:
  dbseeder seed <source> <destination> <url>
  dbseeder update <destination> <url>
  dbseeder (-h | --help | --version)
Options:
  -h --help     Show this screen.
  <source> a file location to a .sde file. eg: "connections\\WRI on PROD.sde"
  <destination> a file location to a .sde file. eg: "connections\\WRI on DEV.sde"
  <url> the base uri of the web api. eg: "http://localhost/wri/" or "https://wrimaps.at.utah.gov/WRI_AT/"
'''

import sys
from dbseeder import Seeder
from docopt import docopt


def main():
    arguments = docopt(__doc__, version='4.1.1')

    locations = {
        'source': arguments['<source>'],
        'destination': arguments['<destination>']
    }

    seeder = Seeder(locations, arguments['<url>'])

    if arguments['seed']:
        return seeder.process()
    elif arguments['update']:
        return seeder.update()

if __name__ == '__main__':
    sys.exit(main())
