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


def teste():
    print("merda")


class Graph(object):
    def __init__(self, node_array: list):
        self.graph = node_array

    def create_nodes(self, values=[]):
        nodes = []
        for value in values:
            nodes.append(Node(value))
        return nodes

    def create_relationship(self, node, nodes: list):
        edges = nodes

        for edge in edges:
            node.add_edge(edge)
        return edges

    def breadth_search(self, initial_node: Node, max_layer=0):
        def enqueue(node):
            queue.append(node)

        def dequeue():
            return queue.pop(0)

        queue = []
        distance = 0

        # realiza uma copia, para nao afetar a variavel original
        node = deepcopy(initial_node)

        # realiza busca em largura dos nos alcancaveis a partir do no principal
        if node.visited == False:
            distance = 0
            node.layer = distance
            enqueue(node)
            node.visited = True

            while len(queue) != 0 and distance <= max_layer:
                u = dequeue()

                if u.layer == distance:
                    distance += 1

                for v in u.edges:
                    print(v.value)
                    if not hasattr(v, 'visited') or v.visited == False:
                        v.visited = True
                        v.layer = distance
                        enqueue(v)

        def automatic_generation(self, qtt_edges: int):
            max_edges = len(self.graph)*(len(self.graph) - 1) / 2
