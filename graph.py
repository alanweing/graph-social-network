
class Vertex:

    UNKNOWN = 0
    KNOWN_CONNECTION = 1
    FRIEND_CONNECTION = 2
    FAMILY_CONNECTION = 3

    def __init__(self, uuid):
        self._uuid = uuid
        self.adjacent = {}
        self.user = None

    def __str__(self):
        return "({}) adjacent to: ".format(self.uuid) + str([x.uuid for x in self.adjacent]) + ' ' + self.user.__str__()

    @property
    def uuid(self):
        return self._uuid

    @property
    def connections(self):
        return [connection_uuid for connection_uuid in self.adjacent]
        # for uuid in self.adjacent:
        #     yield uuid
        # return self.adjacent

    def create_connection(self, uuid, weight=0):
        """
        :param uuid: unique identifier
        :param weight: weight of the connection
        :return: True if the connection is successful, False if it already exists
        :rtype: bool
        """
        if uuid not in self.adjacent:
            self.adjacent[uuid] = weight
            return True
        return False

    def update_connection_weight(self, uuid, new_weight):
        """
        :param uuid:
        :param new_weight:
        :return:
        """
        if uuid in self.adjacent:
            self.adjacent[uuid] = new_weight
            return True
        return False

    def delete_connection(self, connection):
        return self.adjacent.pop(connection, None)

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

    def __str__(self):
        str_ = ''
        for vertex in self.vertex_dictionary:
            str_ += self.get_vertex(vertex).__str__() + '\n\n'
        return str_

    def create_vertex(self, uuid):
        self.number_of_vertices += 1
        new_vertex = Vertex(uuid)
        self.vertex_dictionary[uuid] = new_vertex
        return new_vertex

    def get_vertex(self, uuid):
        """
        :param uuid: unique identifier
        :return: a vertex object
        :rtype: Vertex
        """
        if uuid in self.vertex_dictionary:
            return self.vertex_dictionary[uuid]
        return None

    def delete_vertex(self, uuid):
        if uuid in self.vertex_dictionary:
            delete_ = self.vertex_dictionary[uuid]
            for vertex_ in delete_.connections:
                if vertex_ is not None:
                    vertex_.delete_connection(delete_)
            vertex_ = self.vertex_dictionary.pop(uuid, None)
            if vertex_ is not None:
                self.number_of_vertices -= 1
            return vertex_
        return None

    def create_edge(self, start, end, cost=0):
        if start not in self.vertex_dictionary:
            self.create_vertex(start)
        if end not in self.vertex_dictionary:
            self.create_vertex(end)
        self.get_vertex(start).create_connection(self.get_vertex(end), cost)
        self.get_vertex(end).create_connection(self.get_vertex(start), cost)

    def delete_edge(self, start, end):
        self.get_vertex(start).delete_connection(self.get_vertex(end))
        self.get_vertex(end).delete_connection(self.get_vertex(start))

    def search_common_connections(self):
        # for vertex in self.vertex_dictionary:
        pass

    def is_circular_path(self, needle, haystack=None, current_vertex=None, path=list()):
        if haystack is None:
            haystack = list()
            i = 1
            current_vertex = self.vertex_dictionary.get(0, None)
            while current_vertex is None:
                current_vertex = self.vertex_dictionary.get(i, None)
                i += 1
            path.append(current_vertex)
        haystack.append(current_vertex)
        connections = current_vertex.connections

