from copy import deepcopy
import random
from modules.config import *


colors = [RED, BLUE, BLACK]


class Edge(object):
    index = 0
    color_no_path_tracking = BLACK
    color_path_tracking = LIGHT_BLUE
    color_path_tracked = YELLOW

    def __init__(self):
        self.start = (0, 0)
        self.end = (0, 0)
        self.color = BLACK
        self.value = Edge.index
        Edge.index += 1


class Node(object):
    indexes_used = []
    color_path_tracking = LIGHT_BLUE
    color_path_tracked = GREEN
    node_radius = 20

    def __init__(self, value):
        try:
            if value in self.indexes_used:
                raise AttributeError
            self.value = value
            Node.indexes_used.append(value)
        except AttributeError:
            print('value node (%d) already used' % (value))
            exit()
        self.neighbors = []
        self.color = None
        self.__original_color = None
        self.posX = None
        self.posY = None

    @property
    def original_color(self):
        return self.__original_color

    @original_color.setter
    def original_color(self, new_color):
        self.__original_color = new_color
        self.color = self.__original_color

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
        self.array_nodes_posX = []
        self.array_nodes_posY = []

    def __set_positions(self):
        ''''
            add positions preventing colisions
        '''
        min_distance = Node.node_radius * 3
        posValid = False
        while posValid != True:
            posX = random.randint(
                Node.node_radius, SCREEN_WIDTH - Node.node_radius)
            posY = random.randint(
                Node.node_radius, SCREEN_HEIGHT - Node.node_radius)

            # verify positions
            invalid = False
            for (pX, pY) in zip(self.array_nodes_posX, self.array_nodes_posY):
                if abs(pX - posX) < min_distance and abs(pY - posY) < min_distance:
                    invalid = True
                    break
            if invalid == False:
                posValid = True
        # add occupied positions
        self.array_nodes_posX.append(posX)
        self.array_nodes_posY.append(posY)
        return (posX, posY)

    def create_nodes(self, screen, values=[]):
        nodes = []
        for value in values:
            nodes.append(Node(value))
        self.make_nodes_screen(screen, nodes)
        self.nodes.extend(nodes)
        return nodes

    def make_nodes_screen(self, screen, nodes: list):
        for node in nodes:
            node.original_color = colors[random.randint(0, len(colors) - 1)]
            node.posX, node.posY = self.__set_positions()
            node_aux = screen.create_node(node)

    def create_relationship(self, screen, node, nodes: list):
        neighbors = nodes

        for neighbor in neighbors:
            edge = self.__make_edge_screen(screen, node, neighbor)
            node.add_neighbor(neighbor, edge)
            neighbor.add_neighbor(node, edge)
            self.edges.append(edge)

        return neighbors

    def __make_edge_screen(self, screen, node1, node2):
        edge = Edge()
        edge.start = (node1.posX, node1.posY)
        edge.end = (node2.posX, node2.posY)
        screen.add_edge(node1, node2, edge)
        return edge

    def __change_color_edge(self, edge, color):
        '''
            Funcao para alterar a cor de uma edge no graph original
        '''
        edge_select = self.edges[edge.value]
        edge_select.color = color

    def __paint_track_edges(self, child_node):
        '''
            Funcao para pintar o caminho do node filho ate o node pai,
            utilizando a arvore gerada pela breadth_search
        '''
        if hasattr(child_node.parent, 'edge') and hasattr(child_node.parent, 'node'):
            self.__change_color_edge(
                child_node.parent.edge, child_node.parent.edge.color_path_tracked)
            self.__paint_track_edges(child_node.parent.node)

    def __add_child_tree(self, parent_node, child_node, edge):
        '''
            arvore temporaria para salvar o melhor caminho do initial_node para end_node
        '''
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
            # if current_node.value == initial_node.value:
            if current_node.value == end_node.value:
                screen.paint_node(
                    initial_node, Node.color_path_tracked)
                screen.paint_node(end_node, Node.color_path_tracked)
                self.__paint_track_edges(current_node)
                break

            for neighbor in current_node.neighbors:
                if not hasattr(neighbor.node, 'visited') or neighbor.node.visited == False:
                    enqueue(neighbor.node)
                    # adiciona nodes vizinhos como filhos do node da camada anterior
                    self.__add_child_tree(
                        current_node, neighbor.node, neighbor.edge)
            if len(queue) == 0:
                print('Impossivel ligar os dois nodes')

    def __return_random_nodes(self, node, qtt_edges_remainder):
        '''
            Retorna uma lista de nodes aleatoriamente
        '''
        max_neighbors = len(self.nodes) - 1
        max_size = max_neighbors if max_neighbors < qtt_edges_remainder else qtt_edges_remainder
        size_list = random.randint(0, max_size)
        array_nodes = []
        print(node.value, ' -> [', end='')
        for n in range(size_list):
            while True:
                # node escolhido da lista nao pode ser ele mesmo e nem ser repetido
                node_picked = self.nodes[random.randint(
                    0, len(self.nodes) - 1)]
                if node_picked != node and node_picked not in (array_nodes):
                    break

            print(node_picked.value, ', ', end='')
            array_nodes.append(node_picked)
        print(']')
        return array_nodes

    def __automatic_generation_edges(self, screen, nodes: list, qtt_edges):
        qtt_edges_remainder = qtt_edges
        qtt_nodes = len(nodes)
        index_node = 0
        while qtt_edges_remainder > 0:
            node = nodes[index_node]
            neighbors = self.__return_random_nodes(node, qtt_edges_remainder)
            qtt_edges_remainder -= len(neighbors)
            self.create_relationship(screen, node, neighbors)
            index_node = (index_node + 1) % (qtt_nodes)

    def automatic_generation_graph(self, screen, qtt_nodes: int, qtt_edges: int):
        print('generating graph #########################')
        max_edges = int((qtt_nodes*(qtt_nodes - 1)) / 2)
        try:
            if qtt_edges > max_edges:
                print(qtt_edges, ' -> ', max_edges)
                raise ValueError

            values = []
            nodes = []
            for n in range(qtt_nodes):
                values.append(n)

            nodes = self.create_nodes(screen, values)
            self.__automatic_generation_edges(screen, nodes, qtt_edges)

        except ValueError:
            print('qtt edges is bigger than max edges possible')
            exit()

    def __test(self):
        print('test')
