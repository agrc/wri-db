#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''ArcGIS Press
Usage:
  dbseeder seed <source> <destination>
  dbseeder (-h | --help)
Options:
  -h --help     Show this screen.
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

    seeder = Seeder(locations)

    if arguments['seed']:
        return seeder.process()

if __name__ == '__main__':
    sys.exit(main())
