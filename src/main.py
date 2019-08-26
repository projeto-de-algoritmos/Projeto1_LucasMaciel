from graph import Graph, Node
import draw_screen
import sys

running = True


def main():
    values = [1, 2, 3, 4, 5, 6]
    nodes = []
    graph = Graph(nodes)
    nodes = graph.create_nodes(values)

    graph.create_relationship(nodes[0], nodes[1:5])

    # print(nodes[0].get_value_edges())

    screen = draw_screen.Screen(graph)

    global running
    running = True
    screen.start()

    while running:
        screen.keysListener()

        screen.refresh()


main()
