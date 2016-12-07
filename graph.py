
class Vertex:
    def __init__(self, uuid):
        self._uuid = uuid
        self.adjacent = {}
        self.user = None

    def __str__(self):
        return "{} adjacent: ".format(self.uuid) + str([x.id for x in self.adjacent]) + self.user.__str__()

    @property
    def uuid(self):
        return self._uuid

    @property
    def friends(self):
        return self.adjacent.keys()

    def add_friend(self, friend_uuid, weight=0):
        if friend_uuid not in self.adjacent:
            self.adjacent[friend_uuid] = weight
            return True
        return False

    def get_uuid(self):
        return self.uuid

    def get_weight(self, friend_uuid):
        return self.adjacent[friend_uuid]


class Graph:
    def __init__(self):
        self.vertex_dictionary = {}
        self.number_of_vertices = 0

    def __iter__(self):
        return iter(self.vertex_dictionary.values())

    def add_vertex(self, uuid):
        self.number_of_vertices += 1
        new_vertex = Vertex(uuid)
        self.vertex_dictionary[uuid] = new_vertex
        return new_vertex

    def get_vertex(self, uuid):
        if uuid in self.vertex_dictionary:
            return self.vertex_dictionary[uuid]
        return None

    def add_edge(self, start, end, cost=0):
        if start not in self.vertex_dictionary:
            self.add_vertex(start)
        if end not in self.vertex_dictionary:
            self.add_vertex(end)
        self.vertex_dictionary[start].add_neighbor(self.vertex_dictionary[end], cost)
        self.vertex_dictionary[end].add_neighbor(self.vertex_dictionary[start], cost)
