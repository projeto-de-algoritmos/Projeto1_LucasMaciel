from copy import deepcopy

BLACK = (0, 0, 0)
YELLOW = (255, 166, 0)


class Edge(object):
    index = 0

    def __init__(self):
        self.start = (0, 0)
        self.end = (0, 0)
        self.color = BLACK
        self.value = Edge.index
        Edge.index += 1


class Node(object):
    indexes_used = []

    def __init__(self, value):
        try:
            if value in self.indexes_used:
                raise AttributeError
            self.value = value
            Node.indexes_used.append(value)
        except:
            print('value node (%d) already used' % (value))
            exit()
        self.neighbors = []
        self.color = None
        self.posX = None
        self.posY = None

    def add_neighbor(self, node, edge):
        neighbor = type('', (), {})()
        neighbor.node = node
        neighbor.edge = edge
        self.neighbors.append(neighbor)

    def get_value_neighbors(self):
        values = []
        for neighbor in self.neighbors:
            values.append(neighbor.value)
        return values


class Graph(object):
    def __init__(self):
        self.nodes = []
        self.edges = []

    def create_nodes(self, screen, values=[]):
        nodes = []
        for value in values:
            nodes.append(Node(value))
        self.make_nodes_screen(screen, nodes)
        self.nodes.extend(nodes)
        return nodes

    def make_nodes_screen(self, screen, nodes: list):
        for node in nodes:
            node_aux = screen.create_node(node)

    def create_relationship(self, screen, node, nodes: list):
        neighbors = nodes

        for neighbor in neighbors:
            edge = self.make_edge_screen(screen, node, neighbor)
            node.add_neighbor(neighbor, edge)
            neighbor.add_neighbor(node, edge)
            self.edges.append(edge)

        return neighbors

    def make_edge_screen(self, screen, node1, node2):
        edge = Edge()
        # print(edge.value)
        screen.add_edge(node1, node2, edge)
        return edge

    def change_color_edge(self, edge):
        '''
            Função para alterar a cor de uma edge
        '''
        edge_select = self.edges[edge.value]
        edge_select.color = YELLOW

    def breadth_search(self, screen, initial_node: Node, end_node: Node):
        queue = []
        distance = 0

        def enqueue(node):
            queue.append(node)

        def dequeue():
            return queue.pop(0)

        # realiza uma copia, para nao afetar a variavel original
        node = deepcopy(initial_node)

        # realiza busca em largura dos nos alcancaveis a partir do no principal
        enqueue(node)
        node.visited = True

        while len(queue) > 0:
            current_node = dequeue()
            if current_node.value == initial_node.value:
                print("PAINT %d #################################################" % (
                    current_node.value))
                screen.paint_node(initial_node, (0, 255, 0))
            if current_node.value == end_node.value:
                print("PAINT %d #################################################" % (
                    current_node.value))
                screen.paint_node(end_node, (0, 255, 0))
                print(current_node.visited)
                break

            for neighbor in current_node.neighbors:
                if not hasattr(neighbor.node, 'visited') or neighbor.node.visited == False:
                    neighbor.node.visited = True
                    enqueue(neighbor.node)
                    # alterar cor no grafo original
                    self.change_color_edge(neighbor.edge)

        def automatic_generation(self, qtt_neighbors: int):
            max_neighbors = len(self.graph)*(len(self.graph) - 1) / 2
