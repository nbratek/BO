import json
from models import Group, Table


def input_data_reader(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"File {path} is not a valid JSON.")
    except FileNotFoundError:
        raise ValueError(f"File {path} not found.")
    try:
        groups = []
        for group_data in data['groups']:
            group = Group(group_data['count'], group_data['preferences'])
            groups.append(group)
        tables = []
        for table_data in data['tables']:
            table = Table(table_data['capacity'], table_data['features'])
            tables.append(table)
    except KeyError as e:
        raise ValueError(f"Missing expected data key: {e}")

    return groups, tables
