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
        screen.add_edge(node1, node2, edge)
        return edge

    def change_color_edge(self, edge):
        '''
            Funcao para alterar a cor de uma edge no graph original
        '''
        edge_select = self.edges[edge.value]
        edge_select.color = YELLOW

    def paint_track_edges(self, child_node):
        '''
            Funcao para pintar o caminho do node filho ate o node pai,
            utilizando a arvore gerada pela breadth_search
        '''
        if hasattr(child_node.parent, 'edge') and hasattr(child_node.parent, 'node'):
            self.change_color_edge(child_node.parent.edge)
            self.paint_track_edges(child_node.parent.node)

    def add_child_tree(self, parent_node, child_node, edge):
        '''
            arvore temporaria para salvar o melhor caminho do initial_node para end_node
        '''
        print(parent_node.value, ' -> ', child_node.value)
        parent_node.childs.append(child_node)
        # child_node.parent = parent_node
        child_node.parent.edge = edge
        child_node.parent.node = parent_node

    def breadth_search(self, screen, initial_node: Node, end_node: Node):
        queue = []
        distance = 0

        def enqueue(node):
            node.visited = True
            # atributos para usar na arovore temporaria
            node.childs = []
            node.parent = type('', (), {})()
            queue.append(node)

        def dequeue():
            return queue.pop(0)

        # realiza uma copia, para nao afetar a variavel original
        node = deepcopy(initial_node)

        # realiza busca em largura dos nodes alcancaveis a partir do node principal
        enqueue(node)

        while len(queue) > 0:
            current_node = dequeue()
            if current_node.value == initial_node.value:
                screen.paint_node(initial_node, (0, 255, 0))
            if current_node.value == end_node.value:
                screen.paint_node(end_node, (0, 255, 0))
                print('end node: ', current_node.value)
                print('parent of end node: ', current_node.parent.node.value)
                self.paint_track_edges(current_node)
                break

            for neighbor in current_node.neighbors:
                if not hasattr(neighbor.node, 'visited') or neighbor.node.visited == False:
                    enqueue(neighbor.node)
                    # adiciona nodes vizinhos como filhos do node da camada anterior
                    self.add_child_tree(
                        current_node, neighbor.node, neighbor.edge)

        def automatic_generation(self, qtt_neighbors: int):
            max_edges = len(self.graph)*(len(self.graph) - 1) / 2
