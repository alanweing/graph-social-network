from graph import Vertex, Graph
from user import User
from util._input import Input
from util._print import _print, colorize, danger, Color, warning, info, success

# Método: instanciado
# Funcao: nao instanciado


class Program:
    """Classe responsável por emular um termial e executar as funções e métodos"""
    online = False
    commands = ["create", "read", "update", "delete", "info", "exit"]
    line = "$> "

    def __init__(self):
        self.users_graph = Graph()
        self.current_uuid = 0

    def start(self):
        Program.online = True
        self.start_emulator()

    @staticmethod
    def stop():
        Program.online = False

    """Essa é a função reponsável por pegar o input do usuário"""
    def start_emulator(self):
        while Program.online:
            command = Input()
            command.get(message=Program.line, _type=Input.STRING)
            command = command.last_input.lower().split()
            if command[0] in Program.commands:
                self.command_handler(command)
            else:
                danger("Unrecognized command '%s'" % ' '.join(x for x in command))

    def command_handler(self, command):
        try:
            object_ = command[1]
        except IndexError:
            danger("Missing arguments!")
            return
        _input = Input()
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
                new_vertex = self.users_graph.add_vertex(user_object.uuid)
                new_vertex.user = user_object
                print(new_vertex)
            else:
                danger("Unrecognized command '%s'" % ' '.join(x for x in command))
        elif command[0] == "read":
            pass
        elif command[0] == "update":
            pass
        elif command[0] == "delete":
            pass
        elif command[0] == "info":
            pass
        elif command[0] == "exit":
            pass

    def get_uuid(self):
        uuid = self.current_uuid
        self.current_uuid += 1
        return uuid



def main():
    # p = Program()
    # p.start()
    # test_user = User("Alan", 1)
    # test_user.age = 22
    # test_user.music = "aloha"
    # test_user.music = "asd"
    # test_user.music = 21
    # print(test_user)


    g = Graph()
    #
    v = g.add_vertex(0)
    v.add_friend(1)
    v.add_friend(1)
    print(v.friends)
    print(v.__dict__)
    # g.add_vertex(2)
    # g.add_vertex(3)
    # g.add_vertex(4)
    #
    # g.add_edge(0, 1)
    # g.add_edge(0, 2)
    # g.add_edge(1, 2)
    # g.add_edge(2, 3)
    # g.add_edge(2, 4)
    #
    # for v in g:
    #     for w in v.get_connections():
    #         vid = v.get_id()
    #         wid = w.get_id()
    #         print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))
    #
    # for v in g:
    #     print('g.vert_dict[%s]=%s' % (v.get_id(), g.vertex_dictionary[v.get_id()]))

if __name__ == "__main__":
    main()
