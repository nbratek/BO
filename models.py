class Group:
    def __init__(self, count, reservation, preferences):
        self.count = count
        self.reservation = reservation
        self.preferences = preferences


class Table:
    def __init__(self, capacity, features=None):
        self.capacity = capacity
        self.features = features if features is not None else {}


class Gene:
    def __init__(self, group, table_id, group_id):
        self.group = group
        self.table_id = table_id
        self.group_id = group_id

    def __str__(self):
        return f"Table {self.table_id} with {self.group.count} people (Group {self.group_id})"



