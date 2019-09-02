import sys
from modules.graph import Graph, Node, Edge
from modules.screen_manager import Screen

running = True


def main():
    global running
    screen = Screen()
    graph = Graph(screen)

    # start screen and add function to generate graph
    screen.start(graph.automatic_generation_graph)
    screen.set_search_algorithm(graph.breadth_search)
    running = True

    # graph.automatic_generation_graph(2, 1)

    print('path trackings #########################')
    screen.refresh()


main()
