import random
import sys
from graph import Graph, Node
from draw_screen import Screen

running = True


def make_nodes(screen: Screen, nodes: list):
    for node in nodes:
        node_aux = screen.create_node()
        node.color = node_aux.color
        node.index = node_aux.index
        node.posX = node_aux.posX
        node.posY = node_aux.posY


def make_edges(screen: Screen, graph: Graph, node, nodes: list):
    graph.create_relationship(node, nodes)
    for node_edge in nodes:
        screen.add_edge(node, node_edge)


def main():
    global running
    graph = Graph()
    screen = Screen(graph)
    values = [1, 2, 3, 4, 5, 6]
    nodes = []

    screen.start()
    running = True

    nodes = graph.create_nodes(values)
    make_nodes(screen, nodes)
    make_edges(screen, graph, nodes[0], nodes[1:6])

    while running:
        screen.keysListener()
        screen.refresh()


main()
