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

    db = {
      'source': arguments['<source>'],
      'destination': arguments['<destination>']
    }

    seeder = Seeder()

    if arguments['seed']:
        return seeder.process(db)

if __name__ == '__main__':
    sys.exit(main())
