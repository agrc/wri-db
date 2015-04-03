#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
models
----------------------------------
The basic models
'''


class TreatmentArea(object):

    def __init__(self):
        super(TreatmentArea, self).__init__()

        self.source = 'WRI.WRIADMIN.WRITREATMENTAREA'
        self.destination = 'POLY'

    schema = {
        'OBJECTID': {
            'type': 'int',
            'map': 'FeatureID',
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
        'Completed': {
            'type': 'string',
            'map': 'Completed',
            'lookup': 'complete',
            'order': 4
        },
        'Status': {
            'type': 'int',
            'map': 'Status',
            'order': 5
        },
        'SHAPE@': {
            'type': 'shape',
            'map': 'SHAPE@',
            'order': 6
        }
    }

    def destination_fields(self):
        items = sorted(map(lambda x: {x['order']: x['map']}, self.schema.values()))

        fields = []
        for field in items:
            fields.append(field.values()[0])

        return fields

    def order_destination_values(self, attributes):
        return [
            attributes['FeatureID'],
            attributes['GUID'],
            attributes['Project_FK'],
            attributes['TypeDescription'],
            attributes['Completed'],
            attributes['Status']
        ]

    def source_fields(self):
        items = sorted(map(lambda x: {x[1]['order']: x[0]}, self.schema.items()))

        fields = []
        for field in items:
            fields.append(field.values()[0])

        return fields


class Table(object):

    def __init__(self, table):
        super(Table, self).__init__()

    rollup = {
        'BICYCLIST_INVOLVED': {
            'type': 'bit',
            'map': 'bicycle'
        },
        'COMMERCIAL_MOTOR_VEH_INVOLVED': {
            'type': 'bit',
            'map': 'commercial_vehicle'
        },
        'CRASH_DATETIME': {
            'type': 'date',
            'map': 'date'
        },
        'CRASH_ID': {
            'type': 'int',
            'map': 'id'
        },
        'DOMESTIC_ANIMAL_RELATED': {
            'type': 'bit',
            'map': 'animal_domestic'
        },
        'DUI': {
            'type': 'bit',
            'map': 'dui'
        },
        'IMPROPER_RESTRAINT': {
            'type': 'bit',
            'map': 'improper_restraint'
        },
        'INTERSECTION_RELATED': {
            'type': 'bit',
            'map': 'intersection'
        },
        'MOTORCYCLE_INVOLVED': {
            'type': 'bit',
            'map': 'motorcycle'
        },
        'NIGHT_DARK_CONDITION': {
            'type': 'bit',
            'map': 'dark'
        },
        'OLDER_DRIVER_INVOLVED': {
            'type': 'bit',
            'map': 'elder'
        },
        'OVERTURN_ROLLOVER': {
            'type': 'bit',
            'map': 'rollover'
        },
        'PEDESTRIAN_INVOLVED': {
            'type': 'bit',
            'map': 'pedestrian'
        },
        'TEENAGE_DRIVER_INVOLVED': {
            'type': 'bit',
            'map': 'teenager'
        },
        'WILD_ANIMAL_RELATED': {
            'type': 'bit',
            'map': 'animal_wild'
        }
    }

    @staticmethod
    def rollup_schema_ordering(d):
        return [
            d['id'],
            d['date'],
            d['pedestrian'],
            d['bicycle'],
            d['motorcycle'],
            d['improper_restraint'],
            d['dui'],
            d['intersection'],
            d['animal_wild'],
            d['animal_domestic'],
            d['rollover'],
            d['commercial_vehicle'],
            d['teenager'],
            d['elder'],
            d['dark']
        ]

    rollup_input_keys = rollup.keys()
    rollup_etl_keys = map(lambda x: x['map'], rollup.values())

    crash = {
        'CASE_NUMBER': {
            'type': 'string',
            'map': 'case_number'
        },
        'CITY': {
            'type': 'string',
            'map': 'city'
        },
        'COUNTY_NAME': {
            'type': 'string',
            'map': 'county'
        },
        'CRASH_DATETIME': {
            'type': 'date',
            'map': 'date'
        },
        'CRASH_ID': {
            'type': 'int',
            'map': 'crash_id'
        },
        'CRASH_SEVERITY_ID': {
            'type': 'int',
            'map': 'severity',
            'lookup': 'severity'
        },
        'DAY': {
            'type': 'int',
            'map': 'day'
        },
        'FIRST_HARMFUL_EVENT_ID': {
            'type': 'int',
            'map': 'event',
            'lookup': 'event'
        },
        'HOUR': {
            'type': 'int',
            'map': 'hour'
        },
        'MAIN_ROAD_NAME': {
            'type': 'string',
            'map': 'road_name'
        },
        'MANNER_COLLISION_ID': {
            'type': 'int',
            'map': 'collision_type',
            'lookup': 'collision_type'
        },
        'MILEPOINT': {
            'type': 'float',
            'map': 'milepost'
        },
        'MINUTE': {
            'type': 'int',
            'map': 'minute'
        },
        'MONTH': {
            'type': 'int',
            'map': 'month'
        },
        'OFFICER_DEPARTMENT_CODE': {
            'type': 'string',
            'map': 'officer_department'
        },
        'OFFICER_DEPARTMENT_NAME': {
            'type': 'string',
            'map': 'officer_name'
        },
        'ROADWAY_SURF_CONDITION_ID': {
            'type': 'int',
            'map': 'road_condition',
            'lookup': 'road_condition'
        },
        'ROUTE_NUMBER': {
            'type': 'int',
            'map': 'route_number'
        },
        'UTM_X': {
            'type': 'float',
            'map': 'utm_x'
        },
        'UTM_Y': {
            'type': 'float',
            'map': 'utm_y'
        },
        'WEATHER_CONDITION_ID': {
            'type': 'int',
            'map': 'weather_condition',
            'lookup': 'weather_condition'
        },
        'WORK_ZONE_RELATED': {
            'type': 'bit',
            'map': 'construction'
        },
        'YEAR': {
            'type': 'int',
            'map': 'year'
        }
    }

    @staticmethod
    def crash_schema_ordering(d):
        geometry = (d['utm_x'], d['utm_y'])
        return [
            geometry,
            d['crash_id'],
            d['date'],
            d['year'],
            d['month'],
            d['day'],
            d['hour'],
            d['minute'],
            d['construction'],
            d['weather_condition'],
            d['road_condition'],
            d['event'],
            d['collision_type'],
            d['severity'],
            d['case_number'],
            d['officer_name'],
            d['officer_department'],
            d['road_name'],
            d['route_number'],
            d['milepost'],
            d['city'],
            d['county'],
            d['utm_x'],
            d['utm_y']
        ]

    crash_fields = ['shape@',
                    'crash_id',
                    'date',
                    'year',
                    'month',
                    'day',
                    'hour',
                    'minute',
                    'construction',
                    'weather_condition',
                    'road_condition',
                    'event',
                    'collision_type',
                    'severity',
                    'case_number',
                    'officer_name',
                    'officer_department',
                    'road_name',
                    'route_number',
                    'milepost',
                    'city',
                    'county',
                    'utm_x',
                    'utm_y']
    crash_input_keys = crash.keys()
    crash_etl_keys = map(lambda x: x['map'], crash.values())


class Lookup(object):

    def __init__(self):
        super(Lookup, self).__init__()

    treatment_area = {
        1: 'Terrestrial',
        2: 'Aquatic'
    }

    complete = {
        1: 'Proposal',
        2: 'Project',
        3: 'Complete',
        4: 'Not Funded',
        5: 'Cancelled'
    }
