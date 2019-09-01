import pygame
import pygame.gfxdraw
from pygame.locals import *
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
        pygame.gfxdraw.filled_circle(
            self.screen, 100, 100, 50, YELLOW)

    def create_node(self, node):

        self.nodes.append(node)

        return node

    def add_edge(self, edge):
        # create edge of a node
        self.edges.append(edge)

    def remove_edge(self):
        # remove an edge
        self.edges.pop()

    def draw(self, clock_fps=30):
        # redraw screen
        self.screen.fill(LIGHT_GRAY)
        # Draw edges
        for edge in self.edges:
            pygame.draw.line(
                self.screen, edge.color, (edge.node_start.posX, edge.node_start.posY), (edge.node_end.posX, edge.node_end.posY), 3)
        # Draw Nodes
        for node in self.nodes:
            pygame.gfxdraw.filled_circle(
                self.screen, node.posX, node.posY, NODE_RADIUS, node.color)

        pygame.display.update()
        self.clock.tick(clock_fps)

    def paint_node_selected(self, node, color=YELLOW):
        node.color = color

    def clear_path(self):
        '''
            apagar caminho da busca anterior
        '''
        for edge in self.edges:
            edge.color = edge.no_path_tracking_color

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
                self.enqueue_nodes[0], self.enqueue_nodes[1])
            self.enqueue_nodes = []

    def selected_node(self, position):
        psx = position[0]
        psy = position[1]
        for node in self.nodes:
            radius = NODE_RADIUS
            if (psx > node.posX - radius and psx < node.posX + radius and psy > node.posY - radius and psy < node.posY + radius):
                return node
        return None

    def change_nodes_pos(self, change_posX, change_posY):
        for node in self.nodes:
            node.posX += change_posX
            node.posY += change_posY

    def change_node_pos(self, node, change_posX, change_posY):
        node.posX += change_posX
        node.posY += change_posY

    def keys_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEMOTION:
                if event.buttons[2]:
                    # clicked on right button and moving
                    position = pygame.mouse.get_pos()
                    rel = event.rel
                    self.change_nodes_pos(rel[0], rel[1])
                if event.buttons[0]:
                    # clicked on left button to drag node
                    position = pygame.mouse.get_pos()
                    node = self.selected_node(position)
                    if node != None:
                        rel = event.rel
                        self.change_node_pos(node, rel[0], rel[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                # if left button is clicked
                position = pygame.mouse.get_pos()
                node = self.selected_node(position)
                if node != None:
                    self.cache_enqueue_selected_nodes(node)

    def refresh(self):
        while 1:
            self.keys_listener()
            self.draw()
