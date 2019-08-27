import pygame
import time
import random
from graph import Graph

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
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
        posX = random.randint(0, SCREEN_WIDTH - 20)
        posY = random.randint(0, SCREEN_HEIGHT - 20)

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

    def refresh(self):

        if pygame.mouse.get_pressed()[0]:
            # if left button is clicked
            position = pygame.mouse.get_pos()
            self.selectBlock(position)
        self.draw()

    def draw(self):
        # Draw edges
        for edge in self.edges:
            pygame.draw.line(screen, BLACK, edge.start, edge.end, 2)
        # Draw Nodes
        for node in self.nodes:
            pygame.draw.circle(screen, node.color,
                               (node.posX, node.posY), self.node_radius)
        pygame.display.update()

    def keysListener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
