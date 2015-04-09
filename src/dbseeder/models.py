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
        self.owner = 'dbo'
        self.owner = 'WRIADMIN'
        self.ignore_if_incomplete = ['SHAPE@', 'Status']
        self.where_clause = '1=1'

    def set_incomplete(self, incomplete):
        if incomplete:
            self.source += '_INCOMPLETE'
            self.where_clause = 'Completed = 0'

        self.incomplete = incomplete

    def destination_fields(self):
        items = sorted(map(lambda x: {x['order']: x}, self.schema.values()))

        fields = []
        for field in items:
            #: skip for incomplete tables
            if self.incomplete and field.values()[0]['map'] in self.ignore_if_incomplete:
                continue

            #: drop index if incomplete is True
            if self.incomplete:
                field.values()[0]['order'] = field.values()[0]['order'] - 1

            fields.append(field.values()[0]['map'])

        return fields

    def source_fields(self):
        items = sorted(map(lambda x: {x[1]['order']: x[0]}, self.schema.items()))

        fields = []
        for field in items:
            #: skip shape for incomplete tables
            if self.incomplete and field.values()[0] in self.ignore_if_incomplete:
                continue

            #: drop index if incomplete is True
            if self.incomplete:
                current_key = field.keys()[0]
                new_key = current_key - 1

                if new_key not in field:
                    field[new_key] = field[current_key]
                    del field[current_key]

            #: ignore fields that have no source
            if field.values()[0].startswith('*'):
                continue

            fields.append(field.values()[0])

        return fields

    def unmapped_fields(self):
        items = map(lambda x: {x[1]['order']: x[0]}, self.schema.items())

        fields = []
        for field in items:
            #: skip shape for incomplete tables
            if self.incomplete and field.values()[0] in self.ignore_if_incomplete:
                continue

            #: drop index if incomplete is True
            if self.incomplete:
                current_key = field.keys()[0]
                new_key = current_key - 1

                if new_key not in field:
                    field[new_key] = field[current_key]
                    del field[current_key]

            #: ignore fields that have a source
            if not field.values()[0].startswith('*'):
                continue

            fields.append((field.values()[0], field.keys()[0]))

        return fields

    def etl_fields(self):
        items = filter(lambda x: 'etl' in x, self.schema.values())
        items = map(lambda x: (x['order'], x['etl']), items)

        return items


class TreatmentArea(Table):

    def __init__(self, incomplete=True):
        super(TreatmentArea, self).__init__()

        self.source = 'WRI.{}.WRITREATMENTAREA'.format(self.owner)
        self.set_incomplete(incomplete)

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


class TreatmentArea_Final(Table):

    def __init__(self):
        super(TreatmentArea_Final, self).__init__()

        self.source = 'WRI.{}.WRIFINALTREATMENTAREA'.format(self.owner)
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
            'CompletedProject_FK': {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 5
            }
        }


class AffectedArea(Table):

    def __init__(self, incomplete=False):
        super(AffectedArea, self).__init__()

        self.source = 'WRI.{}.WRIAFFECTEDAREA'.format(self.owner)
        self.set_incomplete(incomplete)

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


class AffectedArea_Final(Table):

    def __init__(self):
        super(AffectedArea_Final, self).__init__()

        self.source = 'WRI.{}.WRIFINALAFFECTEDAREA'.format(self.owner)
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
            'CompletedProject_FK': {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 5
            }
        }


class Points(Table):

    def __init__(self, incomplete=False):
        super(Points, self).__init__()

        self.source = 'WRI.{}.WRIPOINTS'.format(self.owner)
        self.set_incomplete(incomplete)

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


class Points_Final(Table):

    def __init__(self):
        super(Points_Final, self).__init__()

        self.source = 'WRI.{}.WRIFINALPOINTS'.format(self.owner)
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
            'CompletedProject_FK': {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 6
            }
        }


class Guzzler(Table):

    def __init__(self, incomplete=False):
        super(Guzzler, self).__init__()

        self.source = 'WRI.{}.WRIGUZZLER'.format(self.owner)
        self.set_incomplete(incomplete)

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


class Guzzler_Final(Table):

    def __init__(self):
        super(Guzzler_Final, self).__init__()

        self.source = 'WRI.{}.WRIFINALGUZZLER'.format(self.owner)
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
            'CompletedProject_FK': {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 7
            }
        }


class Dam(Table):

    def __init__(self, incomplete=False):
        super(Dam, self).__init__()

        self.source = 'WRI.{}.WRIDam'.format(self.owner)
        self.set_incomplete(incomplete)

        self.destination = 'LINE'
        self.schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0,
                'etl': {
                    'in': 'POLY',
                    'out': 'LINE',
                    'method': 'poly_to_line'
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


class Dam_Final(Table):

    def __init__(self):
        super(Dam_Final, self).__init__()

        self.source = 'WRI.{}.WRIFINALDAM'.format(self.owner)
        self.destination = 'LINE'
        self.schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0,
                'etl': {
                    'in': 'POLY',
                    'out': 'LINE',
                    'method': 'poly_to_line'
                }
            },
            'GUID': {
                'type': 'unique',
                'map': 'GUID',
                'order': 1
            },
            'CompletedProject_FK': {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 6
            }
        }


class Fence(Table):

    def __init__(self, incomplete=False):
        super(Fence, self).__init__()

        self.source = 'WRI.{}.WRIFENCE'.format(self.owner)
        self.set_incomplete(incomplete)

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


class Fence_Final(Table):

    def __init__(self):
        super(Fence_Final, self).__init__()

        self.source = 'WRI.{}.WRIFINALFENCE'.format(self.owner)
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
            'CompletedProject_FK': {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 7
            }
        }


class Pipeline(Table):

    def __init__(self, incomplete=False):
        super(Pipeline, self).__init__()

        self.source = 'WRI.{}.WRIPipeline'.format(self.owner)
        self.set_incomplete(incomplete)

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


class Pipeline_Final(Table):

    def __init__(self):
        super(Pipeline_Final, self).__init__()

        self.source = 'WRI.{}.WRIFINALPIPELINE'.format(self.owner)
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
            'CompletedProject_FK': {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
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
