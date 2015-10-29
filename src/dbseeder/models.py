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

    def source_fields(self, strip_bang=True, strip_unmapped=True):
        items = sorted(map(lambda x: {x[1]['order']: x[0]}, self.schema.items()))

        fields = []
        for field in items:
            value = field.values()[0]
            #: ignore fields that have no source
            if value.startswith('*') and strip_unmapped:
                continue

            #: add duplicate field
            if value.startswith('!') and strip_bang:
                value = value.lstrip('!')

            fields.append(value)

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

    def merge_data(self, row):
        data = []
        destination = self.destination_fields()
        source = self.source_fields(strip_bang=False, strip_unmapped=False)
        row_index = 0

        for index, field in enumerate(source):
            #: if the field is unmappable append None
            if field.startswith('*'):
                data.append((field, destination[index], None))

                continue

            #: get row value
            value = row[row_index]

            item = (field, destination[index], value)
            data.append(item)
            row_index += 1

        return data


class Points(Table):

    def __init__(self, final=False):
        super(Points, self).__init__()

        schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0,
                'etl': {
                    'method': 'point_to_multipoint'
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
            'Type': {
                'type': 'string',
                'map': 'TypeDescription',
                'lookup': 'other_points',
                'order': 3
            },
            '!Type': {
                'type': 'int',
                'map': 'TypeCode',
                'lookup': 'other_points_code',
                'order': 4
            },
            'Description': {
                'type': 'string',
                'map': 'Description',
                'action': 'strip',
                'order': 5
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 6
            },
            '!status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 7
            },
            '!Project_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 8
            }
        }

        final_schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0,
                'etl': {
                    'method': 'point_to_multipoint'
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
            'Type': {
                'type': 'string',
                'map': 'TypeDescription',
                'lookup': 'other_points',
                'order': 3
            },
            '!Type': {
                'type': 'string',
                'map': 'TypeCode',
                'lookup': 'other_points_code',
                'order': 4
            },
            'Description': {
                'type': 'string',
                'map': 'Description',
                'action': 'strip',
                'order': 5
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 6
            },
            '*StatusCode': {
                'type': 'string',
                'map': 'StatusCode',
                'value': 5,
                'order': 7
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 8
            }
        }

        self.name = self.format_source_table('{1}Points as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}POINTS', [self.owner, final])
        self.destination = '{}.POINT'.format('dbo')
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
                'order': 0,
                'etl': {
                    'method': 'point_to_multipoint'
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
                'map': 'TypeDescription',
                'value': 'Guzzler',
                'order': 3
            },
            '*TypeCode': {
                'type': 'string',
                'map': 'TypeCode',
                'value': 5,
                'order': 4
            },
            'GuzzlerType': {
                'type': 'string',
                'map': 'FeatureSubTypeDescription',
                'lookup': 'guzzler_type',
                'order': 5
            },
            '!GuzzlerType': {
                'type': 'int',
                'map': 'FeatureSubTypeID',
                'action': 'guzzler_type_code',
                'order': 6
            },
            'GuzzlerAction': {
                'type': 'string',
                'map': 'ActionDescription',
                'lookup': 'structure_action',
                'order': 7
            },
            '!GuzzlerAction': {
                'type': 'int',
                'map': 'ActionID',
                'action': 'structure_action_code',
                'order': 8
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 9
            },
            '!Status': {
                'type': 'string',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 10
            },
            '!Project_Fk': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 11
            }
        }

        final_schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0,
                'etl': {
                    'method': 'point_to_multipoint'
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
                'map': 'TypeDescription',
                'value': 'Guzzler',
                'order': 3
            },
            '*TypeCode': {
                'type': 'string',
                'map': 'TypeCode',
                'value': 5,
                'order': 4
            },
            'GuzzlerType': {
                'type': 'string',
                'map': 'FeatureSubTypeDescription',
                'lookup': 'guzzler_type',
                'order': 5
            },
            '!GuzzlerType': {
                'type': 'int',
                'map': 'FeatureSubTypeID',
                'action': 'guzzler_type_code',
                'order': 6
            },
            'GuzzlerAction': {
                'type': 'string',
                'map': 'ActionDescription',
                'lookup': 'structure_action',
                'order': 7
            },
            '!GuzzlerAction': {
                'type': 'int',
                'map': 'ActionID',
                'action': 'structure_action_code',
                'order': 8
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 9
            },
            '*StatusCode': {
                'type': 'string',
                'map': 'StatusCode',
                'value': 5,
                'order': 10
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 11
            }
        }

        self.name = self.format_source_table('{1}Guzzler as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}GUZZLER', [self.owner, final])
        self.destination = '{}.POINT'.format('dbo')
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
                'map': 'TypeDescription',
                'value': 'Fence',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 10,
                'order': 4
            },
            'FenceType': {
                'type': 'string',
                'map': 'FeatureSubTypeDescription',
                'lookup': 'fence_type',
                'order': 5
            },
            '!FenceType': {
                'type': 'int',
                'map': 'FeatureSubTypeID',
                'action': 'fence_type_code',
                'order': 6
            },
            'FenceAction': {
                'type': 'string',
                'map': 'ActionDescription',
                'lookup': 'structure_action',
                'order': 7
            },
            '!FenceAction': {
                'type': 'int',
                'map': 'ActionID',
                'action': 'structure_action_code',
                'order': 8
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 9
            },
            '!status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 10
            },
            '!Project_Fk': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 11
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
                'map': 'TypeDescription',
                'value': 'Fence',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 10,
                'order': 4
            },
            'FenceType': {
                'type': 'string',
                'map': 'FeatureSubTypeDescription',
                'lookup': 'fence_type',
                'order': 5
            },
            '!FenceType': {
                'type': 'int',
                'map': 'FeatureSubTypeID',
                'action': 'fence_type_code',
                'order': 6
            },
            'FenceAction': {
                'type': 'string',
                'map': 'ActionDescription',
                'lookup': 'structure_action',
                'order': 7
            },
            '!FenceAction': {
                'type': 'int',
                'map': 'ActionID',
                'action': 'structure_action_code',
                'order': 8
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 9
            },
            '*StatusCode': {
                'type': 'int',
                'map': 'StatusCode',
                'value': 5,
                'order': 10
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 11
            }
        }

        self.name = self.format_source_table('{1}Fence as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}FENCE', [self.owner, final])
        self.destination = '{}.LINE'.format('dbo')
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
                'map': 'TypeDescription',
                'value': 'Pipeline',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 11,
                'order': 4
            },
            'PipelineType': {
                'type': 'string',
                'map': 'FeatureSubTypeDescription',
                'lookup': 'pipeline_type',
                'order': 5
            },
            '!PipelineType': {
                'type': 'int',
                'map': 'FeatureSubTypeID',
                'action': 'pipeline_type_code',
                'order': 6
            },
            'PipelineAction': {
                'type': 'string',
                'map': 'ActionDescription',
                'lookup': 'structure_action',
                'order': 7
            },
            '!PipelineAction': {
                'type': 'int',
                'map': 'ActionID',
                'action': 'structure_action_code',
                'order': 8
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 9
            },
            '!Status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 10
            },
            '!Project_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 11
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
                'map': 'TypeDescription',
                'value': 'Pipeline',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 11,
                'order': 4
            },
            'PipelineType': {
                'type': 'string',
                'map': 'FeatureSubTypeDescription',
                'lookup': 'pipeline_type',
                'order': 5
            },
            '!PipelineType': {
                'type': 'int',
                'map': 'FeatureSubTypeID',
                'action': 'pipeline_type_code',
                'order': 6
            },
            'PipelineAction': {
                'type': 'string',
                'map': 'ActionDescription',
                'lookup': 'structure_action',
                'order': 7
            },
            '!PipelineAction': {
                'type': 'int',
                'map': 'ActionID',
                'action': 'structure_action_code',
                'order': 8
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 9
            },
            '*StatusCode': {
                'type': 'int',
                'map': 'StatusCode',
                'value': 5,
                'order': 10
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 11
            }
        }

        self.name = self.format_source_table('{1}Pipeline as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}PIPELINE', [self.owner, final])
        self.destination = '{}.LINE'.format('dbo')
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
                'map': 'TypeDescription',
                'value': 'Dam',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 12,
                'order': 4
            },
            'DamAction': {
                'type': 'string',
                'map': 'ActionDescription',
                'lookup': 'structure_action',
                'order': 5
            },
            '!DamAction': {
                'type': 'int',
                'map': 'ActionID',
                'action': 'structure_action_code',
                'order': 6
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 7
            },
            '!Status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 8
            },
            '!Project_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 9
            }
        }

        final_schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0,
                'etl': {
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
                'map': 'TypeDescription',
                'value': 'Dam',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 12,
                'order': 4
            },
            'DamAction': {
                'type': 'string',
                'map': 'ActionDescription',
                'lookup': 'structure_action',
                'order': 5
            },
            '!DamAction': {
                'type': 'int',
                'map': 'ActionID',
                'action': 'structure_action_code',
                'order': 6
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 7
            },
            '*StatusCode': {
                'type': 'int',
                'map': 'StatusCode',
                'value': 5,
                'order': 8
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 9
            }
        }

        self.name = self.format_source_table('{1}Dam as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}DAM', [self.owner, final])
        self.destination = '{}.LINE'.format('dbo')
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
                'map': 'TypeDescription',
                'value': 'Affected Area',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 3,
                'order': 4
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 5
            },
            '!Status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 6
            },
            '!Project_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
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
                'map': 'TypeDescription',
                'value': 'Affected Area',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 3,
                'order': 4
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 5
            },
            '*StatusCode': {
                'type': 'int',
                'map': 'StatusCode',
                'value': 5,
                'order': 6
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
            }
        }

        self.name = self.format_source_table('{1}Affected Areas as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}AFFECTEDAREA', [self.owner, final])
        self.destination = '{}.POLY'.format('dbo')
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class AquaticTreatmentArea(Table):

    def __init__(self, final=False):
        super(AquaticTreatmentArea, self).__init__()

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
                'map': 'TypeDescription',
                'lookup': 'treatment_area',
                'order': 3
            },
            '*Type': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 2,
                'order': 4
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 5
            },
            '!Status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 6
            },
            '!Project_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
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
                'map': 'TypeDescription',
                'lookup': 'treatment_area',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 2,
                'order': 4
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 5
            },
            '*StatusCode': {
                'type': 'int',
                'map': 'StatusCode',
                'value': 5,
                'order': 6
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
            }
        }

        self.name = self.format_source_table('{1}Aquatic Treatment Areas as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}TREATMENTAREA', [self.owner, final])
        #: get all aquatic treatments without the fish passage and research action
        self.where_clause = self.format_source_table('Type = 2 and guid not in (select distinct(TreatmentArea_FK) ' +
                                                     'from {0}.WRI{1}AQUATICRIPARIANACTION ' +
                                                     'where ActionCode in (1,6))', [self.owner, final])
        self.destination = '{}.POLY'.format('dbo')
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class Research(Table):

    def __init__(self, final=False):
        super(Research, self).__init__()

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
                'map': 'TypeDescription',
                'value': 'Affected Area',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 3,
                'order': 4
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 5
            },
            '!Status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 6
            },
            '!Project_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
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
                'map': 'TypeDescription',
                'value': 'Affected Area',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 3,
                'order': 4
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 5
            },
            '*StatusCode': {
                'type': 'int',
                'map': 'StatusCode',
                'value': 5,
                'order': 6
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
            }
        }

        self.name = self.format_source_table('{1}Research as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}TREATMENTAREA', [self.owner, final])
        #: get all aquatic treatments with all the research actions
        self.where_clause = self.format_source_table('Type = 2 and guid in (select distinct(TreatmentArea_FK) ' +
                                                     'from {0}.WRI{1}AQUATICRIPARIANACTION where ActionCode = 6)',
                                                     [self.owner, final])
        self.destination = '{}.POLY'.format('dbo')
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class TerrestrialTreatmentArea(Table):

    def __init__(self, final=False):
        super(TerrestrialTreatmentArea, self).__init__()

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
                'map': 'TypeDescription',
                'lookup': 'treatment_area',
                'order': 3
            },
            '*Type': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 1,
                'order': 4
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 5
            },
            '!Status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 6
            },
            '!Project_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
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
                'map': 'TypeDescription',
                'lookup': 'treatment_area',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 1,
                'order': 4
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 5
            },
            '*StatusCode': {
                'type': 'int',
                'map': 'StatusCode',
                'value': 5,
                'order': 6
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
            }
        }

        self.name = self.format_source_table('{1}Terrestrial Treatment Areas as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}TREATMENTAREA', [self.owner, final])
        #: get all Terrestrial treatments without the conservation and fee title
        self.where_clause = self.format_source_table('Type = 1 and guid not in (select distinct(TreatmentArea_FK) ' +
                                                     'from {0}.WRI{1}TerrestrialACTION where ' +
                                                     'ActionCode in (24,25))', [self.owner, final])
        self.destination = '{}.POLY'.format('dbo')
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class FishPassage(Table):

    def __init__(self, final=False):
        super(FishPassage, self).__init__()

        schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0,
                'etl': {
                    'method': ['centroid', 'point_to_multipoint']
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
                'map': 'TypeDescription',
                'value': 'Fish passage structure',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 9,
                'order': 4
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 5
            },
            '!Status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 6
            },
            '!Project_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
            }
        }

        final_schema = {
            'SHAPE@': {
                'type': 'shape',
                'map': 'SHAPE@',
                'order': 0,
                'etl': {
                    'method': ['centroid', 'point_to_multipoint']
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
                'map': 'TypeDescription',
                'value': 'Fish passage structure',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 9,
                'order': 4
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 5
            },
            '*StatusCode': {
                'type': 'int',
                'map': 'StatusCode',
                'value': 5,
                'order': 6
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
            }
        }
        self.name = self.format_source_table('{1}Fish Passage Structure as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}TREATMENTAREA', [self.owner, final])
        #: get all aquatic treatments with the fish passage action
        self.where_clause = self.format_source_table('Type = 2 and guid in (select distinct(TreatmentArea_FK) ' +
                                                     'from {0}.WRI{1}AQUATICRIPARIANACTION where ActionCode = 1)',
                                                     [self.owner, final])
        self.destination = '{}.POINT'.format('dbo')
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class EasementAquisition(Table):

    def __init__(self, final=False):
        super(EasementAquisition, self).__init__()

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
                'map': 'TypeDescription',
                'value': 'Easement/Acquisition',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 4,
                'order': 4
            },
            'Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'lookup': 'status',
                'order': 5
            },
            '!Status': {
                'type': 'int',
                'map': 'StatusCode',
                'lookup': 'status_code',
                'order': 6
            },
            '!Project_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
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
                'map': 'TypeDescription',
                'value': 'Easement/Acquisition',
                'order': 3
            },
            '*TypeCode': {
                'type': 'int',
                'map': 'TypeCode',
                'value': 4,
                'order': 4
            },
            '*Status': {
                'type': 'string',
                'map': 'StatusDescription',
                'value': 'Completed',
                'order': 5
            },
            '*StatusCode': {
                'type': 'int',
                'map': 'StatusCode',
                'value': 5,
                'order': 6
            },
            '!CompletedProject_FK': {
                'map': 'Project_Id',
                'lookup': 'project_id',
                'action': 'stripcurly',
                'order': 7
            }
        }

        self.name = self.format_source_table('{1}Easement/Aquisition as {0}', [self.owner, final])
        self.source = self.format_source_table('{}.WRI{}TREATMENTAREA', [self.owner, final])
        #: get all terrestrial treatments with the easement and fee actions
        self.where_clause = self.format_source_table('Type = 1 and guid in (select distinct(TreatmentArea_FK) ' +
                                                     'from {0}.WRI{1}TerrestrialACTION where ' +
                                                     'ActionCode in (24,25))',
                                                     [self.owner, final])
        self.destination = '{}.POLY'.format('dbo')
        self.schema = self.set_schema(final,
                                      [
                                          schema,
                                          final_schema,
                                      ])


class Lookup(object):

    def __init__(self):
        super(Lookup, self).__init__()

    feature_type = {
        1: 'Terrestrial Treatment Area',
        2: 'Aquatic/Riparian Treatment Area',
        3: 'Affected Area',
        4: 'Easement/Acquisition',
        5: 'Guzzler',
        6: 'Trough',
        7: 'Water control structure',
        8: 'Other point feature',
        9: 'Fish passage structure',
        10: 'Fence',
        11: 'Pipeline',
        12: 'Dam'
    }

    treatment_area = {
        1: 'Terrestrial Treatment Area',
        2: 'Aquatic/Riparian Treatment Area'
    }

    status = {
        1: 'Proposed',
        2: 'Current',
        3: 'Completed',
        4: 'Cancelled',
        5: 'Cancelled',
    }

    new_status = {
        1: 'Draft',
        2: 'Proposed',
        3: 'Current',
        4: 'Pending Completed',
        5: 'Completed',
        6: 'Cancelled'
    }

    original_status = {
        1: 'Proposal',
        2: 'Project',
        3: 'Complete',
        4: 'Not Funded',
        5: 'Cancelled'
    }

    status_code = {
        1: 2,
        2: 3,
        3: 5,
        4: 6,
        5: 6,
    }

    other_points = {
        1: 'Trough',
        2: 'Water control structure',
        3: 'Other point feature'
    }

    other_points_code = {
        1: 6,
        2: 7,
        3: 8
    }

    structure_action = {
        1: 'Maintenance',
        2: 'Modification',
        3: 'Construction',
        4: 'Reconstruction',
        5: 'Removal'
    }

    guzzler_type = {
        1: 'Big game',
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

    new_subtype = {
        'Barbed wire': 1,
        'Buck pole': 2,
        'Let down': 3,
        'Net wire': 4,
        'Pole top': 5,
        'Water gap (stream corridor)': 6,
        'Livestock crossing (stream corridor)': 7,
        'Above surface': 8,
        'Below surface': 9,
        'High hazard': 10,
        'Moderate hazard': 11,
        'Low hazard': 12,
        'No hazard': 13,
        'Big game': 14,
        'Upland game': 15,
        'Big game/Upland game': 16,
        'Other': 17,
        'Barrier (electric)': 18,
        'Barrier (physical)': 19,
        'Rotary drum screen': 20,
        'Flat plate screen': 21,
        'Fish ladder': 22,
        'Culvert': 23
    }

    new_action = {
        'Aerator': 1,
        'Anchor chain': 2,
        'Biological control (of vegetation)': 3,
        'Bulldozing': 4,
        'Bullhog': 5,
        'Cable': 6,
        'Chain harrow': 7,
        'Construction': 8,
        'Disc': 9,
        'Easement/Acquisition': 10,
        'Excavating/Extraction': 11,
        'Forestry practices': 12,
        'Grazing management/changes': 13,
        'Greenstripping': 14,
        'Harrow': 15,
        'Herbicide application': 16,
        'Interseeding': 17,
        'Lake/Wetland/Pond Improvements': 18,
        'Land imprinter': 19,
        'Maintenance': 20,
        'Modification': 21,
        'Mowing': 22,
        'Piscicide Application': 23,
        'Planting/Transplanting': 24,
        'Prescribed fire': 25,
        'Reconstruction': 26,
        'Removal': 27,
        'Road decommissioning': 28,
        'Road/Parking Area Improvements': 29,
        'Roller chopper': 30,
        'Roller Packer': 31,
        'Seeding (primary)': 32,
        'Seeding (secondary/shrub)': 33,
        'Skid-steer mounted tree cutter': 34,
        'Spring Development': 35,
        'Vegetation removal / hand crew': 36,
        'Stream Corridor/Channel Improvements': 37,
        'Vegetation Improvements': 38,
        'Research': 0
    }
