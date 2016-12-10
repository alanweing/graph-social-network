from graph import Vertex, Graph
from user import User, UserGenerator
from util._input import Input
from util._print import _print, colorize, danger, Color, warning, info, success

# Método: instanciado
# Funcao: nao instanciado


class Program:
    """Classe responsável por emular um termial e executar as funções e métodos"""
    online = False
    commands = ["create", "read", "update", "delete", "info", "exit", "block", "clear"]
    line = "  $> "

    def __init__(self):
        self.graph = Graph()
        self.current_uuid = 0
        self.generate_users(6)
        Program.online = True
        self.start_emulator()

    @staticmethod
    def stop():
        Program.online = False

    def start_emulator(self):
        """Essa é a função reponsável por pegar o input do usuário"""
        while Program.online:
            command = Input()
            command.get(message=Program.line, _type=Input.STRING)
            command = command.last_input.lower().split()
            if command[0] in Program.commands:
                self.command_handler(command)
            else:
                danger("Unrecognized command '%s'" % ' '.join(x for x in command))

    def command_handler(self, command):
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
            else:
                danger("Unrecognized command '%s'" % ' '.join(x for x in command))
        elif command[0] == "read":
            pass
        elif command[0] == "update":
            pass
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

            else:
                danger("Unrecognized command '%s'" % ' '.join(x for x in command))

        elif command[0] == "info":
            try:
                if command[1] == "uuid":
                    print("current uuid:", self.current_uuid)
                elif command[1] == "users":
                    print(self.graph)
                elif command[1] == "cycles":
                    print(self.graph.find_cycles())
                elif command[1] == "path":
                    print(self.graph.find_shortest_path(int(command[2]), int(command[3])))
                elif command[1] == "paths":
                    print([path_ for path_ in self.graph.find_paths(int(command[2]), int(command[3]))])
                elif command[1] == "suggest":
                    print([suggestion.uuid for suggestion in self.graph.suggest_connection(int(command[2]))])
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
            exit(0)
        elif command[0] == "clear":
            print(chr(27) + "[2J")
            return

    def get_uuid(self):
        uuid = self.current_uuid
        self.current_uuid += 1
        return uuid

    def create_user(self, user):
        new_vertex = self.graph.create_vertex(user.uuid)
        new_vertex.user = user
        return new_vertex

    def generate_users(self, number_of_users):
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
        start = self.get_vertex_by_input(start)
        end = self.get_vertex_by_input(end)
        if start is None or end is None:
            return False
        self.graph.create_edge(start.uuid, end.uuid, connection_type)
        return True

    def find_vertex(self, *names):
        for name in names:
            print(name)
            vertex_ = self.get_vertex_by_input(name)
            if vertex_ is None:
                danger("User '%s' not found!" % name)
            yield vertex_

    def get_vertex_by_input(self, input_):
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
