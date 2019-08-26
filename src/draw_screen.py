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
        self.board = []

    def start(self):
        pygame.init()
        self.create_node()

    def create_node(self):
        index = 0
        block = type('', (), {})()
        block.body = pygame.rect.Rect((0, 0, 20, 20))
        block.color = colors[random.randint(0, len(colors) - 1)]
        block.index = index
        self.board.append(block)
        index += 1

    def refresh(self):
        screen.fill(WHITE)

        if pygame.mouse.get_pressed()[0]:
            # if left button is clicked
            position = pygame.mouse.get_pos()
            self.selectBlock(position)
        self.draw()

    def draw(self):
        for block in self.board:
            pygame.draw.rect(screen, block.color, block.body)
        pygame.display.update()

    def keysListener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
