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

        self.where_clause = '1=1'

    def format_source_table(self, table, values):
        owner = values[0]
        final = 'FINAL' if values[1] else ''

        return table.format(owner, final)

    def set_schema(self, is_final, available_schemas):
        self.schema = available_schemas[1] if is_final else available_schemas[0]

        return self.schema

    def destination_fields(self):
        items = sorted(map(lambda x: {x['order']: x}, self.schema.values()))

        fields = []
        for field in items:
            fields.append(field.values()[0]['map'])

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
        items = sorted(map(lambda x: {x[1]['order']: x[0]}, self.schema.items()))

        fields = []
        for field in items:
            #: ignore fields that have a source
            if not field.values()[0].startswith('*'):
                continue

            fields.append((field.keys()[0], field.values()[0]))

        return fields

    def etl_fields(self):
        items = filter(lambda x: 'etl' in x, self.schema.values())
        items = map(lambda x: (x['order'], x['etl']), items)

        return items


class Points(Table):

    def __init__(self, final=False):
        super(Points, self).__init__()

        schema = {
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
                'action': 'strip',
                'order': 4
            },
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 5
            }
        }

        final_schema = {
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
                'action': 'strip',
                'order': 4
            },
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 5
            }
        }

        self.source = self.format_source_table('WRI.{}.WRI{}POINTS', [self.owner, final])
        self.destination = 'POINT'
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class Guzzler(Table):

    def __init__(self, final=False):
        super(Guzzler, self).__init__()

        schema = {
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
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 6
            }
        }

        final_schema = {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 6
            }
        }

        self.source = self.format_source_table('WRI.{}.WRI{}GUZZLER', [self.owner, final])
        self.destination = 'POINT'
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class Fence(Table):

    def __init__(self, final=False):
        super(Fence, self).__init__()

        schema = {
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
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 6
            }
        }

        final_schema = {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 6
            }
        }

        self.source = self.format_source_table('WRI.{}.WRI{}FENCE', [self.owner, final])
        self.destination = 'LINE'
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class Pipeline(Table):

    def __init__(self, final=False):
        super(Pipeline, self).__init__()

        schema = {
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
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 6
            }
        }

        final_schema = {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 6
            }
        }

        self.source = self.format_source_table('WRI.{}.WRI{}PIPELINE', [self.owner, final])
        self.destination = 'LINE'
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class Dam(Table):

    def __init__(self, final=False):
        super(Dam, self).__init__()

        schema = {
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
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 5
            }
        }

        final_schema = {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 5
            }
        }

        self.source = self.format_source_table('WRI.{}.WRI{}DAM', [self.owner, final])
        self.destination = 'LINE'
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class AffectedArea(Table):

    def __init__(self, final=False):
        super(AffectedArea, self).__init__()

        schema = {
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
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 4
            }
        }

        final_schema = {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 4
            }
        }

        self.source = self.format_source_table('WRI.{}.WRI{}AFFECTEDAREA', [self.owner, final])
        self.destination = 'POLY'
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class TreatmentArea(Table):

    def __init__(self, final=False):
        super(TreatmentArea, self).__init__()

        schema = {
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
            'Status': {
                'type': 'string',
                'map': 'Status',
                'lookup': 'status',
                'order': 4
            }
        }

        final_schema = {
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
            '*Status': {
                'type': 'string',
                'map': 'Status',
                'value': 'Complete',
                'order': 4
            }
        }

        self.source = self.format_source_table('WRI.{}.WRI{}TREATMENTAREA', [self.owner, final])
        self.destination = 'POLY'
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


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
