import sys
from modules.graph import Graph, Node, Edge
from modules.draw_screen import Screen

running = True


def main():
    global running
    screen = Screen()
    graph = Graph(screen)

    screen.start()
    screen.selected_search_node = graph.breadth_search
    running = True

    graph.automatic_generation_graph(10, 20)

    print('path trackings #########################')
    while running:
        screen.keys_listener()
        screen.refresh()


main()
