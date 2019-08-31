import pygame
import pygame.gfxdraw
import math
import time
import random
from math import cos, sin
from modules.graph import Graph, Node, Edge

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
RED = (255, 0, 0)
BLUE = (0, 0, 250)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 166, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
colors = [RED, BLUE, BLACK]

pygame.display.set_caption("Graph")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class Screen(object):
    def __init__(self, graph: Graph):
        self.graph = graph
        self.nodes = []
        self.edges = []
        self.node_radius = 20
        self.enqueue_nodes = []
        self.array_nodes_posX = []
        self.array_nodes_posY = []

    def start(self):
        pygame.init()
        screen.fill(LIGHT_GRAY)

    def __set_positions(self):
        ''''
            add positions preventing colisions
        '''
        min_distance = self.node_radius * 3
        posValid = False
        while posValid != True:
            posX = random.randint(
                self.node_radius, SCREEN_WIDTH - self.node_radius)
            posY = random.randint(
                self.node_radius, SCREEN_HEIGHT - self.node_radius)

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

    def create_node(self, node: Node):
        node.original_color = colors[random.randint(0, len(colors) - 1)]
        node.posX, node.posY = self.__set_positions()

        self.nodes.append(node)

        return node

    def add_edge(self, node1, node2, edge):
        # create edge of a node
        edge.start = (node1.posX, node1.posY)
        edge.end = (node2.posX, node2.posY)
        self.edges.append(edge)

    def __draw(self):
        # Draw edges
        for edge in self.edges:
            pygame.draw.line(
                screen, edge.color, (edge.start), (edge.end), 3)
            # pygame.gfxdraw.line(
            #     screen, edge.start[0], edge.start[1], edge.end[0], edge.end[1], edge.color)
        # Draw Nodes
        for node in self.nodes:
            pygame.gfxdraw.filled_circle(
                screen, node.posX, node.posY, self.node_radius, node.color)
        pygame.display.update()

    def paint_node(self, node, color=YELLOW):
        node.color = color

    def clear_path(self):
        '''
            apagar caminho da busca anterior
        '''
        for (edge, node) in zip(self.edges, self.nodes):
            edge.color = Edge.color_no_path_tracking
            node.color = node.original_color

    def cache_enqueue_selected_nodes(self, node):
        '''
            Enqueue until two nodes before activate breadth_search between nodes
        '''
        if len(self.enqueue_nodes) == 0:
            self.clear_path()
            self.paint_node(node)

        if len(self.enqueue_nodes) == 0 or self.enqueue_nodes[0] != node:
            self.enqueue_nodes.append(node)
        for node in self.enqueue_nodes:
            print(node.value, end=", ")
        print()
        if len(self.enqueue_nodes) >= 2:
            self.graph.breadth_search(
                self, self.enqueue_nodes[0], self.enqueue_nodes[1])
            self.enqueue_nodes = []

    def selected_node(self, position):
        psx = position[0]
        psy = position[1]
        radius = self.node_radius
        for node in self.nodes:
            if (psx > node.posX - radius and psx < node.posX + radius and psy > node.posY - radius and psy < node.posY + radius):
                self.cache_enqueue_selected_nodes(node)
                break

    def keys_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if left button is clicked
                position = pygame.mouse.get_pos()
                self.selected_node(position)

    def refresh(self):
        self.__draw()
