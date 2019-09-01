from copy import deepcopy
import random
from modules.config import *


colors = [RED]


class Edge(object):
    index = 0
    no_path_tracking_color = DARK_GRAY
    path_tracking_color = LIGHT_BLUE
    path_tracked_color = YELLOW

    def __init__(self):
        self.start = (0, 0)
        self.end = (0, 0)
        self.color = Edge.no_path_tracking_color
        self.value = Edge.index
        Edge.index += 1


class Node(object):
    indexes_used = []
    path_tracking_color = LIGHT_BLUE
    path_tracked_color = GREEN
    path_tracked_middle_color = YELLOW
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
    def __init__(self, screen):
        self.screen = screen
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

    def create_nodes(self, values=[]):
        nodes = []
        for value in values:
            nodes.append(Node(value))
        self.make_nodes_screen(nodes)
        self.nodes.extend(nodes)
        return nodes

    def make_nodes_screen(self, nodes: list):
        for node in nodes:
            node.original_color = colors[random.randint(0, len(colors) - 1)]
            node.posX, node.posY = self.__set_positions()
            node_aux = self.screen.create_node(node)

    def create_relationship(self, node, nodes: list):
        neighbors = nodes

        for neighbor in neighbors:
            edge = self.__make_edge_screen(
                ((node.posX, node.posY)), (neighbor.posX, neighbor.posY))
            node.add_neighbor(neighbor, edge)
            neighbor.add_neighbor(node, edge)
            self.edges.append(edge)

        return neighbors

    def __make_edge_screen(self, node1_pos: tuple, node2_pos: tuple, color=Edge.no_path_tracking_color):
        edge = Edge()
        edge.start = node1_pos
        edge.end = node2_pos
        edge.color = color
        self.screen.add_edge(edge)
        return edge

    def __change_color_node(self, node, color):
        '''
            Funcao para alterar a cor de um node no graph original
        '''
        node_select = self.nodes[node.value]
        node_select.color = color

    def __change_color_edge(self, edge, color):
        '''
            Funcao para alterar a cor de uma edge no graph original
        '''
        edge_select = self.edges[edge.value]
        edge_select.color = color

    def __paint_tracked_edges(self, child_node):
        '''
            Funcao para pintar o caminho do node filho ate o node pai,
            utilizando a arvore gerada pela breadth_search
        '''
        if hasattr(child_node.parent, 'edge') and hasattr(child_node.parent, 'node'):
            self.__paint_tracked_edges(child_node.parent.node)
            self.__change_color_edge(
                child_node.parent.edge, child_node.parent.edge.path_tracked_color)
            if len(child_node.childs) > 0:
                self.__change_color_node(
                    child_node, child_node.path_tracked_middle_color)
            self.screen.draw(3)

    def __tracking_animation(self, start, end):
        def increase_pos(prev_pos, increase): return prev_pos + increase
        def decrease_pos(prev_pos, decrease): return prev_pos - decrease
        # percent of original edge
        percent_original_edge = 0.05
        size_temp_edge = 0
        temp_edge_start = start
        temp_edge_end = temp_edge_start
        size_increment_x = abs(
            end[0] - start[0]) * percent_original_edge
        size_increment_y = abs(
            end[1] - start[1]) * percent_original_edge

        increment_posX = None
        increment_posY = None
        if end[0] > start[0]:
            increment_posX = increase_pos
        else:
            increment_posX = decrease_pos

        if end[1] > start[1]:
            increment_posY = increase_pos
        else:
            increment_posY = decrease_pos

        temp_edge = self.__make_edge_screen(
            temp_edge_start, temp_edge_end, Edge.path_tracking_color)
        # print('edge start original: ', edge.start)
        # print('edge end original: ', edge.end)
        # print('edge start temp: ', temp_edge_start)
        while(abs(end[0] - temp_edge_end[0]) > size_increment_x
                and abs(end[1] - temp_edge_end[1]) > size_increment_y):

            temp_edge_end = (increment_posX(temp_edge_end[0], size_increment_x),
                             increment_posY(temp_edge_end[1], size_increment_y))
            temp_edge.end = temp_edge_end
            self.screen.draw(16)
            # print('edge end temp: ', temp_edge_end)
        self.screen.remove_edge()
        del temp_edge

    def __paint_tracking_edges(self, edge, node1, node2):
        '''
            Pintar o caminho de busca do node
        '''
        self.__tracking_animation(
            (node1.posX, node1.posY), (node2.posX, node2.posY))

        # finally paint original edge
        self.__change_color_edge(edge, edge.path_tracking_color)
        self.__change_color_node(node2, node2.path_tracking_color)
        self.screen.draw(3)

    def __add_child_tree(self, parent_node, child_node, edge):
        '''
            arvore temporaria para salvar o melhor caminho do initial_node para end_node
        '''
        parent_node.childs.append(child_node)
        # child_node.parent = parent_node
        child_node.parent.edge = edge
        child_node.parent.node = parent_node

    def breadth_search(self, initial_node: Node, end_node: Node):
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
                self.__change_color_node(
                    initial_node, Node.path_tracked_color)
                self.__change_color_node(end_node, Node.path_tracked_color)
                self.__paint_tracked_edges(current_node)
                break

            for neighbor in current_node.neighbors:
                if not hasattr(neighbor.node, 'visited') or neighbor.node.visited == False:
                    enqueue(neighbor.node)
                    # adiciona nodes vizinhos como filhos do node da camada anterior
                    self.__add_child_tree(
                        current_node, neighbor.node, neighbor.edge)
                    self.__paint_tracking_edges(
                        neighbor.edge, current_node, neighbor.node)
            if len(queue) == 0:
                print('Impossivel ligar os dois nodes')

    def __return_random_nodes(self, node, qtt_average, qtt_edges_remainder):
        '''
            Retorna uma lista de nodes aleatoriamente
        '''
        max_neighbors = len(self.nodes) - 1
        max_size = max_neighbors if max_neighbors < qtt_edges_remainder else qtt_edges_remainder
        size_list = random.randint(0, qtt_average)
        array_nodes = []
        print(node.value, ' -> [', end='')
        # neighbors already exists
        neighbor_already = []
        for neighbor in node.neighbors:
            neighbor_already.append(neighbor.node)

        for n in range(size_list):
            while True:
                # node escolhido da lista nao pode ser ele mesmo e nem ser repetido
                node_picked = self.nodes[random.randint(
                    0, len(self.nodes) - 1)]
                if node_picked != node and node_picked not in (array_nodes) and node_picked not in neighbor_already:
                    break

            print(node_picked.value, ', ', end='')
            array_nodes.append(node_picked)
        print(']')
        return array_nodes

    def __automatic_generation_edges(self, nodes: list, qtt_edges):
        qtt_edges_remainder = qtt_edges
        qtt_average = int(qtt_edges/len(self.nodes))
        qtt_nodes = len(nodes)
        index_node = 0
        while qtt_edges_remainder > 0:
            node = nodes[index_node]
            neighbors = self.__return_random_nodes(
                node, qtt_average, qtt_edges_remainder)
            qtt_edges_remainder -= len(neighbors)
            self.create_relationship(node, neighbors)
            index_node = (index_node + 1) % (qtt_nodes)

    def automatic_generation_graph(self, qtt_nodes: int, qtt_edges: int):
        print('generating graph #########################')
        max_edges = int((qtt_nodes*(qtt_nodes - 1)) / 2)
        try:
            if qtt_edges > max_edges:
                print(qtt_edges, ' -> ', max_edges)
                raise max_edges

            values = []
            nodes = []
            for n in range(qtt_nodes):
                values.append(n)

            nodes = self.create_nodes(values)
            self.__automatic_generation_edges(nodes, qtt_edges)

        except max_edges:
            print('qtt edges is bigger than max edges possible')
            exit()

    def __test(self):
        print('test')
