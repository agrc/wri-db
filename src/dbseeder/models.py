#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
models
----------------------------------
The basic models
'''


class Table(object):

    def __init__(self):
        super(Table, self).__init__()

    def destination_fields(self):
        items = sorted(map(lambda x: {x['order']: x['map']}, self.schema.values()))

        fields = []
        for field in items:
            fields.append(field.values()[0])

        return fields

    def source_fields(self):
        items = sorted(map(lambda x: {x[1]['order']: x[0]}, self.schema.items()))

        fields = []
        for field in items:
            #: ignore fields that have no source
            if field.values()[0].startswith('*'):
                continue

            fields.append(field.values()[0])

        return fields

    def unmapped_fields(self):
        items = map(lambda x: {x[1]['order']: x[0]}, self.schema.items())

        fields = []
        for field in items:
            if not field.values()[0].startswith('*'):
                continue

            fields.append((field.values()[0], field.keys()[0]))

        return fields

    def etl_fields(self):
        items = filter(lambda x: 'etl' in x, self.schema.values())
        items = map(lambda x: (x['order'], x['etl']), items)

        return items


class TreatmentArea(Table):

    def __init__(self):
        super(TreatmentArea, self).__init__()

        self.source = 'WRI.WRIADMIN.WRITREATMENTAREA'
        self.destination = 'POLY'
        self.schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0
            },
            'GUID': {
                'type': 'unique',
                'map': 'GUID',
                'order': 1
            },
            'Project_FK': {
                'type': 'unique',
                'map': 'Project_FK',
                'order': 2
            },
            'Type': {
                'type': 'string',
                'map': 'Type',
                'lookup': 'treatment_area',
                'order': 3
            },
            'Completed': {
                'type': 'string',
                'map': 'Completed',
                'order': 4
            },
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 5
            }
        }


class AffectedArea(Table):

    def __init__(self):
        super(AffectedArea, self).__init__()

        self.source = 'WRI.WRIADMIN.WRIAffectedArea'
        self.destination = 'POLY'
        self.schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0
            },
            'GUID': {
                'type': 'unique',
                'map': 'GUID',
                'order': 1
            },
            'Project_FK': {
                'type': 'unique',
                'map': 'Project_FK',
                'order': 2
            },
            '*Type': {
                'type': 'string',
                'map': 'Type',
                'value': 'Affected Area',
                'order': 3
            },
            'Completed': {
                'type': 'string',
                'map': 'Completed',
                'order': 4
            },
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 5
            }
        }


class Points(Table):

    def __init__(self):
        super(Points, self).__init__()

        self.source = 'WRI.WRIADMIN.WRIPOINTS'
        self.destination = 'POINT'
        self.schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0
            },
            'GUID': {
                'type': 'unique',
                'map': 'GUID',
                'order': 1
            },
            'Project_FK': {
                'type': 'unique',
                'map': 'Project_FK',
                'order': 2
            },
            'Type': {
                'type': 'string',
                'map': 'Type',
                'lookup': 'other_points',
                'order': 3
            },
            'Description': {
                'type': 'string',
                'map': 'Description',
                'order': 4
            },
            'Completed': {
                'type': 'string',
                'map': 'Completed',
                'order': 5
            },
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 6
            }
        }


class Guzzler(Table):

    def __init__(self):
        super(Guzzler, self).__init__()

        self.source = 'WRI.WRIADMIN.WRIGUZZLER'
        self.destination = 'POINT'
        self.schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0
            },
            'GUID': {
                'type': 'unique',
                'map': 'GUID',
                'order': 1
            },
            'Project_FK': {
                'type': 'unique',
                'map': 'Project_FK',
                'order': 2
            },
            '*Type': {
                'type': 'string',
                'map': 'Type',
                'value': 'Guzzler',
                'order': 3
            },
            'GuzzlerType': {
                'type': 'string',
                'map': 'SubType',
                'lookup': 'guzzler_type',
                'order': 4
            },
            'GuzzlerAction': {
                'type': 'string',
                'map': 'Action',
                'lookup': 'structure_action',
                'order': 5
            },
            'Completed': {
                'type': 'string',
                'map': 'Completed',
                'order': 6
            },
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 7
            }
        }


class Dam(Table):

    def __init__(self):
        super(Dam, self).__init__()

        self.source = 'WRI.WRIADMIN.WRIDam'
        self.destination = 'POINT'
        self.schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0,
                'etl': {
                    'in': 'POLY',
                    'out': 'POINT',
                    'method': 'centroid'
                }
            },
            'GUID': {
                'type': 'unique',
                'map': 'GUID',
                'order': 1
            },
            'Project_FK': {
                'type': 'unique',
                'map': 'Project_FK',
                'order': 2
            },
            '*Type': {
                'type': 'string',
                'map': 'Type',
                'value': 'Dam',
                'order': 3
            },
            'DamAction': {
                'type': 'string',
                'map': 'Action',
                'lookup': 'structure_action',
                'order': 4
            },
            'Completed': {
                'type': 'string',
                'map': 'Completed',
                'order': 5
            },
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 6
            }
        }


class Fence(Table):

    def __init__(self):
        super(Fence, self).__init__()

        self.source = 'WRI.WRIADMIN.WRIFENCE'
        self.destination = 'LINE'
        self.schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0
            },
            'GUID': {
                'type': 'unique',
                'map': 'GUID',
                'order': 1
            },
            'Project_FK': {
                'type': 'unique',
                'map': 'Project_FK',
                'order': 2
            },
            '*Type': {
                'type': 'string',
                'map': 'Type',
                'value': 'Fence',
                'order': 3
            },
            'FenceType': {
                'type': 'string',
                'map': 'SubType',
                'lookup': 'fence_type',
                'order': 4
            },
            'FenceAction': {
                'type': 'string',
                'map': 'Action',
                'lookup': 'structure_action',
                'order': 5
            },
            'Completed': {
                'type': 'string',
                'map': 'Completed',
                'order': 6
            },
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 7
            }
        }


class Pipeline(Table):

    def __init__(self):
        super(Pipeline, self).__init__()

        self.source = 'WRI.WRIADMIN.WRIPipeline'
        self.destination = 'LINE'
        self.schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0
            },
            'GUID': {
                'type': 'unique',
                'map': 'GUID',
                'order': 1
            },
            'Project_FK': {
                'type': 'unique',
                'map': 'Project_FK',
                'order': 2
            },
            '*Type': {
                'type': 'string',
                'map': 'Type',
                'value': 'Pipeline',
                'order': 3
            },
            'PipelineType': {
                'type': 'string',
                'map': 'SubType',
                'lookup': 'pipeline_type',
                'order': 4
            },
            'PipelineAction': {
                'type': 'string',
                'map': 'Action',
                'lookup': 'structure_action',
                'order': 5
            },
            'Completed': {
                'type': 'string',
                'map': 'Completed',
                'order': 6
            },
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 7
            }
        }


class Lookup(object):

    def __init__(self):
        super(Lookup, self).__init__()

    treatment_area = {
        1: 'Terrestrial',
        2: 'Aquatic/Riparian'
    }

    status = {
        0: 'Draft',
        1: 'Proposal',
        2: 'Project',
        3: 'Complete',
        4: 'Cancelled',
        5: 'Cancelled'
    }

    other_points = {
        1: 'Trough',
        2: 'Water Control Structure',
        3: 'Other'
    }

    structure_action = {
        1: 'Maintenance',
        2: 'Modification',
        3: 'Construction',
        4: 'Reconstruction',
        5: 'Removal'
    }

    guzzler_type = {
        1: 'Big Game',
        2: 'Other'
    }

    fence_type = {
        1: 'Barbed wire',
        2: 'Buck pole',
        3: 'Let down',
        4: 'Net wire',
        5: 'Pole top',
        99: 'Other'
    }

    pipeline_type = {
        1: 'Above surface',
        2: 'Below surface'
    }
