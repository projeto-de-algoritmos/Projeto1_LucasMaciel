import pygame
import pygame.gfxdraw
import math
import time
import random
from math import cos, sin
from modules.config import *


class Screen(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.nodes = []
        self.edges = []
        self.enqueue_nodes = []
        self.selected_search_node = None

    def start(self):
        pygame.display.set_caption("Graph")
        pygame.init()
        self.screen.fill(LIGHT_GRAY)

    def create_node(self, node):

        self.nodes.append(node)

        return node

    def add_edge(self, node1, node2, edge):
        # create edge of a node
        self.edges.append(edge)

    def draw(self, clock_fps=30):
        # Draw edges
        for edge in self.edges:
            pygame.draw.line(
                self.screen, edge.color, (edge.start), (edge.end), 3)
        # Draw Nodes
        for node in self.nodes:
            pygame.gfxdraw.filled_circle(
                self.screen, node.posX, node.posY, node.node_radius, node.color)
        pygame.display.update()
        self.clock.tick(clock_fps)

    def paint_node_selected(self, node, color=YELLOW):
        node.color = color

    def clear_path(self):
        '''
            apagar caminho da busca anterior
        '''
        for edge in self.edges:
            edge.color = edge.color_no_path_tracking

        for node in self.nodes:
            node.color = node.original_color

    def cache_enqueue_selected_nodes(self, node):
        '''
            Enqueue until two nodes before activate breadth_search between nodes
        '''
        if len(self.enqueue_nodes) == 0:
            self.clear_path()
            self.paint_node_selected(node)

        if len(self.enqueue_nodes) == 0 or self.enqueue_nodes[0] != node:
            self.enqueue_nodes.append(node)
        for node in self.enqueue_nodes:
            print(node.value, end=", ")
        print()
        if len(self.enqueue_nodes) >= 2:
            self.selected_search_node(
                self, self.enqueue_nodes[0], self.enqueue_nodes[1])
            self.enqueue_nodes = []

    def selected_node(self, position):
        psx = position[0]
        psy = position[1]
        for node in self.nodes:
            radius = node.node_radius
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
        self.draw()
