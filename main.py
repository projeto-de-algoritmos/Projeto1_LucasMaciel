import random
import sys
from modules.graph import Graph, Node
from modules.draw_screen import Screen

running = True


def main():
    global running
    graph = Graph()
    screen = Screen(graph)
    values = [1, 2, 3, 4, 5, 6]
    nodes = []

    screen.start()
    running = True

    nodes = graph.create_nodes(screen, values)
    graph.create_relationship(screen, nodes[0], nodes[1:6])

    while running:
        screen.keys_listener()
        screen.refresh()


main()
