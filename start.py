from graph import Vertex, Graph
from user import User, UserGenerator
from util._input import Input
from util._print import _print, colorize, danger, Color, warning, info, success

# Método: instanciado
# Funcao: nao instanciado


class Program:
    """Classe responsável por emular um termial e executar as funções e métodos"""
    online = False
    commands = ["create", "read", "delete", "info", "exit", "block", "clear", "suggest"]
    line = "  $> "

    def __init__(self):
        self.graph = Graph()
        self.current_uuid = 0
        self.generate_users(6)
        self.groups = []
        Program.online = True
        self.start_emulator()

    @staticmethod
    def stop():
        """
        Para o programa principal
        """
        Program.online = False

    def start_emulator(self):
        """Essa é a função reponsável por pegar o input do usuário e assegurar que todos os comando estão tratados"""
        while Program.online:
            command = Input()
            command.get(message=Program.line, _type=Input.STRING)
            command = command.last_input.lower().split()
            try:
                if command[0] in Program.commands:
                    self.command_handler(command)
                else:
                    danger("Unrecognized command '%s'" % ' '.join(x for x in command))
            except IndexError:
                pass

    def command_handler(self, command):
        """
        :param command: lista de comandos dada pelo usuário
        :type command: list
        """
        if command[0] not in ["exit", "clear"]:
            try:
                object_ = command[1]
            except IndexError:
                danger("Missing arguments!")
                return
        _input = Input()

        def get_connection_cost(type_):
            return 1 if type_ == "known" else \
                            2 if type_ == "friend" else \
                            3 if type_ == "family" \
                            else 0

        if command[0] == "create":
            if object_ == "user":
                name_ = _input.get("Name:", Input.STRING)
                age_ = _input.get("Age:", Input.INT)
                gender_ = _input.get("Gender:", Input.STRING, ["male", "female"])
                employed_ = _input.get("Is employed?", Input.STRING, ["yes", "no"])
                musics_ = _input.get("Type your favorite musics, separated by ';'", Input.STRING)
                user_object = User(name_, self.get_uuid())
                user_object.age = age_
                user_object.gender = gender_
                user_object.employed = True if employed_.lower() == "yes" else False
                user_object.music = musics_.split(';')
                new_user = self.create_user(user_object)
                print(new_user)

            elif object_ == "connection":
                success_ = False
                if len(command) == 5:
                    success_ = self.create_connection(command[2], command[3], command[4])
                elif len(command) == 4:
                    success_ = self.create_connection(command[2], command[3],
                                                      get_connection_cost(
                                                          _input.get("Connection type:", Input.STRING,
                                                                     ["known", "friend", "family"])))
                elif len(command) == 3:
                    success_ = self.create_connection(command[2], _input.get("Connect to:", Input.MIXED),
                                                      get_connection_cost(
                                                          _input.get("Connection type:", Input.STRING,
                                                                     ["known", "friend", "family"])))
                elif len(command) == 2:
                    success_ = self.create_connection(_input.get("User:", Input.MIXED),
                                                      _input.get("Connect to:", Input.MIXED),
                                                      get_connection_cost(
                                                          _input.get("Connection type:", Input.STRING,
                                                                     ["known", "friend", "family"])))
                if success_:
                    success("Successful connection!")
                return

            elif object_ == "group":
                has_cycles = self.graph.find_cycles()
                for i, list_ in enumerate(has_cycles):
                    for group_ in self.groups:
                        if [uuid_ for uuid_ in list_ if uuid_ in list(group_.values())[0]]:
                            has_cycles.pop(i)
                if len(has_cycles) == 0:
                    warning("There is no cycle in this graph or all have a group.")
                    return
                if len(has_cycles) > 0:
                    input_ = _input.get("Select a graph subset: {}"
                                        .format([cycle_ for cycle_ in has_cycles]), Input.INT,
                                        [i for i in range(len(has_cycles))])
                    connection_weight = None
                    for i, vertex_ in enumerate(has_cycles[_input.last_input]):
                        vertex_ = self.get_vertex_by_input(vertex_)
                        neighbors = vertex_.connections
                        if i == 0:
                            connection_weight = vertex_.get_weight(self.get_vertex_by_input(list(
                                set([neighbor.uuid for neighbor in neighbors]).intersection(
                                    set(has_cycles[_input.last_input])))[0]))
                        else:
                            for neighbor in neighbors:
                                if neighbor.uuid not in has_cycles[_input.last_input]:
                                    continue
                                connection_weight_ = vertex_.get_weight(neighbor)
                                if connection_weight_ != connection_weight:
                                    for group_ in self.groups:
                                        if [uuid_ for uuid_ in has_cycles[_input.last_input] if
                                                uuid_ in list(group_.values())[0]]:
                                            warning("This group already exists!")
                                            return
                                    print("Cannot suggest a group name!")
                                    group_name = Input().get("Group name:", Input.STRING)
                                    self.groups.append(
                                        {group_name: has_cycles[_input.last_input]})
                                    success("Group '{}' created!".format(group_name))
                                    return
                                else:
                                    connection_weight = connection_weight_
                    for group_ in self.groups:
                        if [uuid_ for uuid_ in has_cycles[_input.last_input] if uuid_ in list(group_.values())[0]]:
                            warning("This group already exists!")
                            return
                    self.groups.append({"{} group {}".format(Vertex.get_connection_type(connection_weight),
                                                             str(len(self.groups))): has_cycles[_input.last_input]})
                    success("Group '{}' created with auto generated name!".format(self.groups[-1]))
                else:
                    danger("The current graph doesn't have a cycle!")
            else:
                danger("Unrecognized command '%s'" % ' '.join(x for x in command))

        elif command[0] == "read":
            try:
                if command[1] == "user":
                    print(self.get_vertex_by_input(command[2]))
                else:
                    as_ = command[2]
                    if as_ == "as":
                        vertex_ = self.get_vertex_by_input(command[3])
                        read_ = self.get_vertex_by_input(command[1])
                        if vertex_ is not None and vertex_ is not False and read_ is not None and read_ is not False:
                            if read_.uuid not in vertex_.connections_list:
                                danger("There are no connection between '%s' and '%s'" % (vertex_.user.name,
                                                                                          read_.user.name))
                                return
                            if vertex_.get_weight(read_) >= 1:
                                colorize("User: %s" % read_.user.name, Color.RED, background=Color.WHITEBG)
                            if vertex_.get_weight(read_) >= 2:
                                colorize("Age: %s" % read_.user.age, Color.RED, background=Color.WHITEBG)
                                colorize("Gender: %s" % read_.user.gender, Color.RED, background=Color.WHITEBG)
                            if vertex_.get_weight(read_) >= 3:
                                colorize("Employed: %s" % str(read_.user.employed), Color.RED, background=Color.WHITEBG)
                                colorize("Favorite musics: {}".format(str([music_ for music_ in read_.user.music])),
                                         Color.RED, background=Color.WHITEBG)
            except IndexError:
                danger("Missing arguments!")
                return

        elif command[0] == "delete":
            if object_ == "user":
                try:
                    vertex_ = self.get_vertex_by_input(command[2])
                    if vertex_ is not None and vertex_ is not False:
                        self.graph.delete_vertex(vertex_.uuid)
                        success("User '%s' (uuid: %d) deleted!" % (vertex_.user.name, vertex_.uuid))
                except IndexError:
                    danger("Please, specify an user to delete")
                    return

            elif object_ == "connection":
                try:
                    start_ = self.get_vertex_by_input(command[2])
                    end_ = self.get_vertex_by_input(command[3])
                    if start_ is not None and start_ is not False and end_ is not None and end_ is not False:
                        self.graph.delete_edge(start_.uuid, end_.uuid)
                        success("Connection deleted!")
                except IndexError:
                    danger("Missing arguments! Usage: 'delete connection start_vertex end_vertex'")
            else:
                danger("Unrecognized command '%s'" % ' '.join(x for x in command))

        elif command[0] == "suggest":
            try:
                if command[1] == "connection":
                    vertex_ = self.get_vertex_by_input(command[2])
                    suggestions = self.graph.suggest_connection(vertex_.uuid)
                    print(*suggestions, sep='\n\n')

            except IndexError:
                danger("Usage: 'suggest connection {user}'")
                return

        elif command[0] == "info":
            try:
                if command[1] == "uuid":
                    print("current uuid:", self.current_uuid)
                elif command[1] == "user":
                    print(self.get_vertex_by_input(command[2]))
                elif command[1] == "users":
                    print(self.graph)
                elif command[1] == "cycles":
                    print(self.graph.find_cycles())
                elif command[1] == "path":
                    print(self.graph.find_shortest_path(int(command[2]), int(command[3])))
                elif command[1] == "paths":
                    print([path_ for path_ in self.graph.find_paths(int(command[2]), int(command[3]))])
                elif command[1] == "suggest":
                    vertex_ = self.get_vertex_by_input(command[2])
                    suggestions = self.graph.suggest_connection(vertex_.uuid)
                    print(*suggestions, sep='\n\n')
                elif command[1] == "connections":
                    try:
                        vertex_ = self.get_vertex_by_input(command[2])
                        if vertex_ is not None and vertex_ is not False:
                            for connection in vertex_.weighted_connections:
                                print(connection)
                    except IndexError:
                        for vertex_ in self.graph.vertex_dictionary.values():
                            for connection in vertex_.weighted_connections:
                                print(connection)
                elif command[1] == "graph":
                    print(self.graph)
                elif command[1] == "groups":
                    for group_ in self.groups:
                        for group_name, group_list in group_.items():
                            colorize("Group: {}".format(group_name), Color.RED, background=Color.WHITEBG, bold=True)
                            for user_uuid in group_list:
                                print(self.get_vertex_by_input(user_uuid), "\n")
            except IndexError:
                danger("Missing arguments!")
                return
            except ValueError:
                danger("Please, enter a valid uuid")
                return

        elif command[0] == "block":
            try:
                start = self.get_vertex_by_input(command[1])
                end = self.get_vertex_by_input(command[2])
                if start is not None and start is not False and end is not None and end is not False:
                    self.graph.delete_edge(start.uuid, end.uuid)
                    success("User %s (uuid: %d) is now blocked!" % (end.user.name, end.uuid))
            except IndexError:
                danger("Missing arguments!")
                return

        elif command[0] == "exit":
            info("Bye")
            Program.stop()

        elif command[0] == "clear":
            print(chr(27) + "[2J")
            return

    def get_uuid(self):
        """
        Assegura que cada usuário criado terá um id único (uuid)
        :return: uuid para o novo usuário
        :rtype: int
        """
        uuid = self.current_uuid
        self.current_uuid += 1
        return uuid

    def create_user(self, user):
        """
        :type user: User
        :param user: Novo usuário a ser adicionado no grafo
        :return: Vértice do grafp
        :rtype: Vertex
        """
        new_vertex = self.graph.create_vertex(user.uuid)
        new_vertex.user = user
        return new_vertex

    def generate_users(self, number_of_users):
        """
        Função desenhada para gerar 6 usuários ao iniciar o programa, podem ser gerados mais, mas devem ser adicionadas
        mais informações em users_list da classe UserGenerator
        :param number_of_users: número de usuários a serem gerados e adicionados ao grafo
        """
        info("generating %d users" % number_of_users)
        users_ = UserGenerator.generate(number_of_users, (self.get_uuid() for _ in range(number_of_users)))
        for user_ in users_:
            vertex = self.create_user(user_)
        if number_of_users == 6:
            self.create_connection(0, 1, Vertex.FRIEND_CONNECTION)
            self.create_connection(0, 2, Vertex.FRIEND_CONNECTION)
            self.create_connection(1, 2, Vertex.FRIEND_CONNECTION)
            self.create_connection(2, 3, Vertex.FAMILY_CONNECTION)
            self.create_connection(3, 4, Vertex.KNOWN_CONNECTION)
            self.create_connection(3, 5, Vertex.FAMILY_CONNECTION)
            self.create_connection(4, 5, Vertex.FAMILY_CONNECTION)

    def create_connection(self, start, end, connection_type):
        """
        :param start: vértice inicial
        :param end:  vértice final
        :param connection_type: tipo da conexão (known, friend ou family)
        :return: True se a conexão foi criada, False se não forem encontrados os vértices
        :rtype: bool
        """
        start = self.get_vertex_by_input(start)
        end = self.get_vertex_by_input(end)
        if start is None or end is None:
            return False
        self.graph.create_edge(start.uuid, end.uuid, connection_type)
        return True

    def find_vertex(self, *names):
        """
        Wildcard function !NOT USED!
        """
        for name in names:
            print(name)
            vertex_ = self.get_vertex_by_input(name)
            if vertex_ is None:
                danger("User '%s' not found!" % name)
            yield vertex_

    def get_vertex_by_input(self, input_):
        """
        :param input_: pode ser tanto um int para uuid ou string para o nome de um usuário
        :type input_: (int,string)
        :return: Um vértice se os dados que o usuário entrar existirem no grafo
        :rtype: Vertex
        """
        try:
            input_ = int(input_)
        except ValueError:
            pass
        vertex_ = False
        type_ = ''
        if isinstance(input_, int):
            vertex_ = self.graph.get_vertex(input_)
            type_ = "uuid"
        elif isinstance(input_, str):
            vertex_ = self.graph.find_vertex_by_user_name(input_)
            type_ = "user"
        if vertex_ is None:
            danger("Cannot find %s '%s'!" % (type_, str(input_)))
            return None
        return vertex_

if __name__ == "__main__":
    Program()
