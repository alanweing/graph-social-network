from graph import Vertex, Graph
from user import User

# Método: instanciado
# Funcao: nao instanciado

class Program:
    """Classe responsável por emular um termial e executar as funções certas"""
    online = False
    commands = []

    def __init__(self):
        pass

    def start(self):
        Program.online = True
        self.start_emulator()

    @staticmethod
    def stop():
        Program.online = False

    """Essa é a função reponsável por pegar o input do usuário"""
    def start_emulator(self):
        try:
            while Program.online:
                pass
        except KeyboardInterrupt:
            pass


def main():
    test_user = User("Alan", 1)
    test_user.age = 22
    test_user.music = "aloha"
    test_user.music = "asd"
    test_user.music = 21
    print(test_user)
    # g = Graph()
    #
    # g.add_vertex(0)
    # g.add_vertex(1)
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
