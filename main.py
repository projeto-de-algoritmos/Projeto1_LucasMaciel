from graph import Graph, Node
import sys


def main():
    values = [1, 2, 3, 4, 5, 6]
    nodes = []
    graph = Graph(nodes)
    nodes = graph.create_nodes(values)

    graph.create_relationship(nodes[0], nodes[1:5])

    print(nodes[0].get_value_edges())


main()
