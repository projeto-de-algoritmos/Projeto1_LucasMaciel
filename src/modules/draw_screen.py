import pygame
import pygame.gfxdraw
import math
import time
import random
from math import cos, sin
from modules.graph import Graph

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 166, 0)
WHITE = (255, 255, 255)
colors = [RED, GREEN, BLACK]

pygame.display.set_caption("Test")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class Screen(object):
    def __init__(self, graph: Graph):
        self.graph = graph
        self.nodes = []
        self.edges = []
        self.node_radius = 20

    def start(self):
        pygame.init()
        screen.fill(WHITE)

    def create_node(self):
        posX = random.randint(
            self.node_radius, SCREEN_WIDTH - self.node_radius)
        posY = random.randint(
            self.node_radius, SCREEN_HEIGHT - self.node_radius)

        node = type('', (), {})()
        node.color = colors[random.randint(0, len(colors) - 1)]
        node.index = len(self.nodes)
        node.posX = posX
        node.posY = posY
        self.nodes.append(node)
        return node

    def add_edge(self, node1, node2):
        # create edge of a node
        edge = type('', (), {})()
        edge.start = (node1.posX, node1.posY)
        edge.end = (node2.posX, node2.posY)
        self.edges.append(edge)

    def draw(self):
        # Draw edges
        for edge in self.edges:
            pygame.gfxdraw.line(
                screen, edge.start[0], edge.start[1], edge.end[0], edge.end[1], BLACK)
        # Draw Nodes
        for node in self.nodes:
            pygame.gfxdraw.filled_circle(
                screen, node.posX, node.posY, self.node_radius, node.color)
        pygame.display.update()

    def paint_node(self, node):
        node.color = YELLOW

    def selectNode(self, position):
        psx = position[0]
        psy = position[1]
        radius = self.node_radius
        for node in self.nodes:
            if (psx > node.posX - radius and psx < node.posX + radius and psy > node.posY - radius and psy < node.posY + radius):
                self.paint_node(node)
                break

    def keysListener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def refresh(self):

        if pygame.mouse.get_pressed()[0]:
            # if left button is clicked
            position = pygame.mouse.get_pos()
            self.selectNode(position)
        self.draw()
