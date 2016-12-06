
class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.payload = {}

    def __str__(self):
        return "{} adjacent: ".format(self.id) + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]


class Graph:
    def __init__(self):
        self.vertex_dictionary = {}
        self.number_of_vertices = 0

    def __iter__(self):
        return iter(self.vertex_dictionary.values())

    def add_vertex(self, node):
        self.number_of_vertices += 1
        new_vertex = Vertex(node)
        self.vertex_dictionary[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vertex_dictionary:
            return self.vertex_dictionary[n]
        return None

    def add_edge(self, start, end, cost=0):
        if start not in self.vertex_dictionary:
            self.add_vertex(start)
        if end not in self.vertex_dictionary:
            self.add_vertex(end)
        self.vertex_dictionary[start].add_neighbor(self.vertex_dictionary[end], cost)
        self.vertex_dictionary[end].add_neighbor(self.vertex_dictionary[start], cost)
