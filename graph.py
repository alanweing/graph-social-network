from sys import getrecursionlimit, setrecursionlimit


class Vertex:
    """
    Classe equivalente ao vértice de um grafo
    """
    UNKNOWN = 0
    KNOWN_CONNECTION = 1
    FRIEND_CONNECTION = 2
    FAMILY_CONNECTION = 3

    def __init__(self, uuid):
        self._uuid = uuid
        self.adjacent = {}
        self.user = None

    def __str__(self):
        return "({}) adjacent to: ".format(self.uuid) + str([x.uuid for x in self.adjacent]) + '\n' + self.user.__str__()

    @property
    def uuid(self):
        return self._uuid

    @property
    def connections(self):
        return [vertex for vertex in self.adjacent]

    @property
    def connections_list(self):
        return [vertex.uuid for vertex, key in self.adjacent.items()]

    @property
    def weighted_connections(self):
        return ["({}) {} -> ({}) {}\t\t{}".format(self.uuid, self.user.name, vertex.uuid, vertex.user.name,
                                                  self.get_connection_type(key)).upper()
                for vertex, key in self.adjacent.items()]

    @staticmethod
    def get_connection_type(key):
        """
        :param key: peso da conexão
        :return: Nome da conexão
        :rtype: str
        """
        return ("Family" if key == 3 else "Friend" if key == 2 else "Known" if key == 1 else "Unknown connection type")\
               + " connection"

    def create_connection(self, vertex, weight=0):
        """
        :param vertex: Vértice a ser conectado
        :param weight: Peso da conexão
        :return: True se a conexão for sucedida, False se não
        :rtype: bool
        """
        if vertex not in self.adjacent:
            self.adjacent[vertex] = weight
            return True
        return False

    def update_connection_weight(self, vertex, new_weight):
        """
        !NOT IMPLEMENTED/NOT USED!
        """
        if vertex in self.adjacent:
            self.adjacent[vertex] = new_weight
            return True
        return False

    def delete_connection(self, connection):
        """
        :param connection: aresta de uma conexão a ser deletada
        :return: conexão recém deletada
        """
        return self.adjacent.pop(connection, None)

    def get_weight(self, vertex):
        """
        :param vertex: Vértice para pegar o peso da conexão
        :return: Peso da conexão
        :rtype: int
        """
        return self.adjacent[vertex]


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

    @property
    def vertices(self):
        return [vertex_ for vertex_ in self.vertex_dictionary]

    def create_vertex(self, uuid):
        """
        :param uuid: Identificador único para o vértice
        :return: Novo vértice, sem conexões
        :rtype: Vertex
        """
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
        """
        :param uuid: identificador do vértice a ser deletado
        :return: vértice recém deletado
        """
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
        """
        Cria uma conexão entre start e end com peso cost
        :param start: vértice inicial
        :param end: vértice final
        :param cost: peso da conexã0
        """
        if start not in self.vertex_dictionary:
            self.create_vertex(start)
        if end not in self.vertex_dictionary:
            self.create_vertex(end)
        self.get_vertex(start).create_connection(self.get_vertex(end), cost)
        self.get_vertex(end).create_connection(self.get_vertex(start), cost)

    def delete_edge(self, start, end):
        """
        deleta uma conxão entre start e end
        :param start: vértice inicial
        :param end: vértice final
        """
        self.get_vertex(start).delete_connection(self.get_vertex(end))
        self.get_vertex(end).delete_connection(self.get_vertex(start))

    def breath_first_search(self, uuid):
        """
        :param uuid: uuid to search for connections
        :return: all possible uuids that can be accessed from start
        :rtype: list
        """
        visited, queue = set(), [uuid]
        while queue:
            vertex_ = queue.pop(0)
            if vertex_ not in visited:
                visited.add(vertex_)
                queue.extend(set(self.vertex_dictionary[vertex_].connections_list) - visited)
        return visited

    def find_paths(self, start, needle):
        """
        :param start: starter uuid
        :param needle: desired uuid to find
        :return: all possible paths to needle
        :rtype: generator
        """
        queue = [(start, [start])]
        while queue:
            (vertex_, path) = queue.pop(0)
            for next_ in set(self.vertex_dictionary[vertex_].connections_list) - set(path):
                if next_ == needle:
                    yield path + [next_]
                else:
                    queue.append((next_, path + [next_]))

    def find_shortest_path(self, start, needle):
        """
        :param start: starter uuid
        :param needle: uuid to find
        :return: shortest path to needle
        :rtype: list
        """
        try:
            return next(self.find_paths(start, needle))
        except StopIteration:
            return None

    def suggest_connection(self, ancestor):
        """
        :param ancestor: vértice para sugerir conexões
        :return: lista de vértices que podem ser adicionados ao ancestor (possuem alguma forma de ligacão entre
        outras conexões)
        """
        ancestor = self.vertex_dictionary[ancestor]
        suggestion_list = []
        for connection in ancestor.connections:
            for sub_connection in connection.connections:
                if sub_connection.uuid not in ancestor.connections_list and sub_connection != ancestor:
                    suggestion_list.append(sub_connection)
        return suggestion_list

    def find_cycle(self):
        """
        :return: list of nodes that make a cycle in the graph
        :rtype: list
        """
        vertices = self.vertex_dictionary
        vertices_list = self.vertices
        visited = {}
        spanning_tree = {}
        cycle = []

        def find_cycle_to_ancestor(vertex, ancestor):
            """
            Find a cycle containing both node and ancestor.
            """
            path = []
            while vertex != ancestor:
                if vertex is None:
                    return []
                path.append(vertex)
                vertex = spanning_tree[vertex]
            path.append(vertex)
            path.reverse()
            return path

        def depth_first_search(vertex):
            """
            Depth-first search sub-function.
            """
            visited[vertex] = 1
            for each in vertices[vertex].connections_list:
                if cycle:
                    return
                if each not in visited:
                    spanning_tree[each] = vertex
                    depth_first_search(each)
                else:
                    if spanning_tree[vertex] != each:
                        cycle.extend(find_cycle_to_ancestor(vertex, each))

        recursion_limit = getrecursionlimit()
        setrecursionlimit(max(len(vertices_list) * 2, recursion_limit))

        for vertex_ in vertices_list:
            if vertex_ not in visited:
                spanning_tree[vertex_] = None
                depth_first_search(vertex_)
                if cycle:
                    setrecursionlimit(recursion_limit)
                    return cycle

        setrecursionlimit(recursion_limit)
        return []

    def find_cycles(self, root=None):
        """
        From NetworkX module
        :param root: Optional vertex, specify one for basis
        :return: A list of cycle lists
        :rtype: list
        """
        vertices = set(self.vertices)
        cycles = []
        while vertices:
            root = vertices.pop() if root is None else root
            stack = [root]
            pred = {root: root}
            used = {root: set()}
            while stack:
                z = stack.pop()
                zused = used[z]
                for nbr in self.vertex_dictionary[z].connections_list:
                    if nbr not in used:
                        pred[nbr] = z
                        stack.append(nbr)
                        used[nbr] = set([z])
                    elif nbr == z:
                        cycles.append(z)
                    elif nbr not in zused:
                        pn = used[nbr]
                        cycle = [nbr, z]
                        p = pred[z]
                        while p not in pn:
                            cycle.append(p)
                            p = pred[p]
                        cycle.append(p)
                        cycles.append(cycle)
                        used[nbr].add(z)
            vertices -= set(pred)
            root = None
        return cycles

    def find_vertex_by_user_name(self, name):
        """
        :param name: nome do usuário
        :return: vértice se existir um vértice com um usuário de nome 'name' None se não encontrar
        """
        for uuid in self.vertex_dictionary:
            if self.vertex_dictionary[uuid].user.name.lower() == str(name):
                return self.vertex_dictionary[uuid]
        return None
