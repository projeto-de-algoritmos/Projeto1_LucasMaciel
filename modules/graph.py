from copy import deepcopy


class Node(object):
    def __init__(self, value):
        self.value = value
        self.edges = []

    def add_edge(self, node):
        self.edges.append(node)

    def get_value_edges(self):
        values = []
        for edge in self.edges:
            values.append(edge.value)
        return values


class Graph(object):
    def __init__(self, node_array: list = []):
        self.graph = node_array
        self.object = []

    def create_nodes(self, screen, values=[]):
        nodes = []
        for value in values:
            nodes.append(Node(value))
        self.make_nodes_screen(screen, nodes)
        return nodes

    def make_nodes_screen(self, screen, nodes: list):
        for node in nodes:
            node_aux = screen.create_node(node)

    def create_relationship(self, screen, node, nodes: list):
        edges = nodes

        for edge in edges:
            node.add_edge(edge)
            edge.add_edge(node)
        self.make_edges_screen(screen, node, nodes)
        return edges

    def make_edges_screen(self, screen, node, nodes: list):
        for node_edge in nodes:
            screen.add_edge(node, node_edge)

    def breadth_search(self, screen, initial_node: Node, end_node: Node):
        queue = []
        distance = 0

        def enqueue(node):
            queue.append(node)

        def dequeue():
            return queue.pop(0)

        # realiza uma copia, para nao afetar a variavel original
        node = initial_node
        # node = deepcopy(initial_node)

        # realiza busca em largura dos nos alcancaveis a partir do no principal
        enqueue(node)
        node.visited = True

        while len(queue) > 0:
            current_node = dequeue()
            if current_node == initial_node or current_node == end_node:
                print("PAINT#################################################")
                screen.paint_node(current_node, (0, 255, 0))
                if current_node == end_node:
                    break

            for neighbor in current_node.edges:
                if not hasattr(neighbor, 'visited') or neighbor.visited == False:
                    neighbor.visited = True
                    enqueue(neighbor)

        def automatic_generation(self, qtt_edges: int):
            max_edges = len(self.graph)*(len(self.graph) - 1) / 2
