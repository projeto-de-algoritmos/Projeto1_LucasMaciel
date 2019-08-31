import sys
from modules.graph import Graph, Node, Edge
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

#     nodes = graph.create_nodes(screen, values)
#     graph.create_relationship(screen, nodes[0], nodes[1:5])
#     graph.create_relationship(screen, nodes[3], [nodes[5]])
    graph.automatic_generation_graph(screen, 50, 50)

    print('path trackings #########################')
    while running:
        screen.keys_listener()
        screen.refresh()


main()
