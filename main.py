import sys
from modules.graph import Graph, Node, Edge
from modules.draw_screen import Screen

running = True


def main():
    global running
    screen = Screen()
    graph = Graph(screen)

    # start screen and add function to generate graph
    screen.start(graph.automatic_generation_graph)
    screen.selected_search_node = graph.breadth_search
    running = True

    # graph.automatic_generation_graph(5, 10)

    print('path trackings #########################')
    screen.refresh()


main()
