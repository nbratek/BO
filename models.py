from math import sqrt

class Group:
    def __init__(self, count, reservation, preferences):
        self.count = count
        self.reservation = reservation
        self.preferences = preferences



class Table:
    def __init__(self, capacity,position, features=None):
        self.capacity = capacity
        self.features = features if features is not None else {}
        self.x, self.y = position
    def distance(self,other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Gene:
    def __init__(self, group, table_id, group_id):
        self.group = group
        self.table_id = table_id
        self.group_id = group_id

    def __eq__(self, other):
        return self.group == other.group and self.table_id == other.table_id and self.group_id == other.table_id

    def __str__(self):
        return f"Group nr.{self.group_id} (count: {self.group.count}) {'(with reservation)' if self.group.reservation else ''} assigned to table nr.{self.table_id}"
        # return f"Table {self.table_id} with {self.group.count} people (Group {self.group_id})"



