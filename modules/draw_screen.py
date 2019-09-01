import pygame
import pygame.gfxdraw
from pygame.locals import *
import math
import time
import random
from math import cos, sin
from modules.config import *


class Button(object):
    def __init__(self, text, posX=100, posY=100, width=50, height=30):
        self.width = width
        self.height = height
        self.posX = posX
        self.posY = posY
        self.box = pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.font = pygame.font.Font(None, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = text
        self.done = False

    def set_pos(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.box = pygame.Rect(self.posX, self.posY, self.width, self.height)

    def draw(self, screen):
        txt_surface = self.font.render(
            self.text, True, self.color)
        width = max(self.width, txt_surface.get_width()+10)
        self.box.w = width
        screen.blit(txt_surface, (self.box.x +
                                  5, self.box.y+5))
        pygame.draw.rect(screen, self.color,
                         self.box, 2)

    def clicked(self):
        self.active = not self.active

    def switch_status(self, event):
        # Change the current color of the input box.
        self.color = self.color_active if self.active else self.color_inactive


class Input(Button):
    def __init__(self, posX=100, posY=100, width=50, height=30):
        self.width = width
        self.height = height
        self.box = pygame.Rect(posX, posY, self.width, self.height)
        self.font = pygame.font.Font(None, 32)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False

    def typing(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode


class Screen(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = None
        self.clock = pygame.time.Clock()
        self.nodes = []
        self.edges = []
        self.enqueue_nodes = []
        self.selected_search_node = None
        self.input_number_nodes = None
        self.input_number_edges = None
        self.button_menu = None
        self.keys_listener_selected = self.keys_listener_menu
        self.draw_screen_selected = self.draw_menu
        self.generate_graph = None
        self.text_warning = ''

    def start(self, generate_graph):
        pygame.display.set_caption("Graph")
        pygame.init()
        self.font = pygame.font.Font(
            'modules/fonts/roboto/Roboto-Black.ttf', 15)
        self.input_number_nodes = Input(100, 100)
        self.input_number_edges = Input(250, 100)
        self.button_menu = Button('OK', 350, 100)
        self.generate_graph = generate_graph

    def create_node(self, node):

        self.nodes.append(node)

        return node

    def add_edge(self, edge):
        # create edge of a node
        self.edges.append(edge)

    def remove_edge(self):
        # remove an edge
        self.edges.pop()

    def paint_node_selected(self, node, color=YELLOW):
        node.color = color

    def clear_path(self):
        '''
            apagar caminho da busca anterior
        '''
        for edge in self.edges:
            edge.color = edge.no_path_tracking_color

        for node in self.nodes:
            node.color = node.original_color

    def cache_enqueue_selected_nodes(self, node):
        '''
            Enqueue until two nodes before activate breadth_search between nodes
        '''
        if len(self.enqueue_nodes) == 0:
            self.clear_path()

        self.paint_node_selected(node)

        if len(self.enqueue_nodes) == 0 or self.enqueue_nodes[0] != node:
            self.enqueue_nodes.append(node)
        for node in self.enqueue_nodes:
            print(node.value, end=", ")
        print()
        if len(self.enqueue_nodes) >= 2:
            self.selected_search_node(
                self.enqueue_nodes[0], self.enqueue_nodes[1])
            self.enqueue_nodes = []

    def selected_node(self, position):
        psx = position[0]
        psy = position[1]
        for node in self.nodes:
            radius = NODE_RADIUS
            if (psx > node.posX - radius and psx < node.posX + radius and psy > node.posY - radius and psy < node.posY + radius):
                return node
        return None

    def change_nodes_pos(self, change_posX, change_posY):
        for node in self.nodes:
            node.posX += change_posX
            node.posY += change_posY

    def change_node_pos(self, node, change_posX, change_posY):
        node.posX += change_posX
        node.posY += change_posY

    def draw_menu(self, clock_fps=30):
        # redraw screen
        self.screen.fill(LIGHT_GRAY)
        # Draw Input box
        self.input_number_nodes.draw(self.screen)
        self.input_number_edges.draw(self.screen)

        # Draw Button
        self.button_menu.draw(self.screen)

        # render labels
        label = self.font.render("N° Nodes:", True, BLACK)
        self.screen.blit(label, (self.input_number_nodes.box.left -
                                 70, self.input_number_nodes.box.top))

        label = self.font.render("N° Edges:", True, BLACK)
        self.screen.blit(label, (self.input_number_edges.box.left -
                                 70, self.input_number_edges.box.top))

        # render warning
        label_warning = self.font.render(self.text_warning, True, RED)
        self.screen.blit(label_warning,
                         (SCREEN_WIDTH / 4, SCREEN_HEIGHT - 100))

        pygame.display.flip()
        self.clock.tick(clock_fps)

    def switch_to_graph(self):
        self.nodes = []
        self.edges = []
        self.generate_graph(int(self.input_number_nodes.text), int(
            self.input_number_edges.text))
        self.keys_listener_selected = self.keys_listener
        self.draw_screen_selected = self.draw
        self.button_menu.text = 'MENU'
        self.button_menu.set_pos(20, SCREEN_HEIGHT - 50)

    def switch_to_menu(self):
        self.keys_listener_selected = self.keys_listener_menu
        self.draw_screen_selected = self.draw_menu
        self.button_menu.text = 'OK'
        self.button_menu.set_pos(350, 100)

    def keys_listener_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if clicked on input_number_nodes
                if self.input_number_nodes.box.collidepoint(event.pos):
                    self.input_number_nodes.clicked()
                else:
                    self.input_number_nodes.active = False
                self.input_number_nodes.switch_status(event)

                # if clicked on input_number_edges
                if self.input_number_edges.box.collidepoint(event.pos):
                    self.input_number_edges.clicked()
                else:
                    self.input_number_edges.active = False
                self.input_number_edges.switch_status(event)

                # if clicked on Button Confirm
                if self.button_menu.box.collidepoint(event.pos):
                    self.button_menu.clicked()
                    # init screen graph
                    try:
                        qtt_nodes = int(self.input_number_nodes.text)
                        qtt_edges = int(self.input_number_edges.text)
                        max_edges = int((qtt_nodes*(qtt_nodes - 1)) / 2)
                        print(qtt_nodes, ' + ', qtt_edges)

                        if self.input_number_nodes.text == '' or self.input_number_edges.text == '':
                            self.text_warning = "Digite o Numero de Nodes e Arestas!"
                        elif qtt_nodes > qtt_edges:
                            self.text_warning = "Numero de Arestas deve ser maior do que o de Nodes!"
                        elif qtt_edges > max_edges:
                            self.text_warning = "Numero de Arestas maior do que o maximo possivel!"
                        else:
                            self.switch_to_graph()
                    except:
                        self.text_warning = "Digite Valores Validos!"
                else:
                    self.button_menu.active = False
                self.button_menu.switch_status(event)

            if event.type == pygame.KEYDOWN:
                # typing on input_number_nodes
                if self.input_number_nodes.active:
                    if event.key == pygame.K_RETURN:
                        self.input_number_nodes.text = ''
                    self.input_number_nodes.typing(event)

                # typing on input_number_edges
                if self.input_number_edges.active:
                    if event.key == pygame.K_RETURN:
                        self.input_number_edges.text = ''
                    self.input_number_edges.typing(event)

    def draw(self, clock_fps=30):
        # redraw screen
        self.screen.fill(LIGHT_GRAY)
        # Draw edges
        for edge in self.edges:
            pygame.draw.line(
                self.screen, edge.color, (edge.node_start.posX, edge.node_start.posY), (edge.node_end.posX, edge.node_end.posY), 3)
        # Draw Nodes
        for node in self.nodes:
            pygame.gfxdraw.filled_circle(
                self.screen, node.posX, node.posY, NODE_RADIUS, node.color)

        # Draw Button Menu
        self.button_menu.draw(self.screen)

        # pygame.display.update()
        pygame.display.flip()
        self.clock.tick(clock_fps)

    def keys_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEMOTION:
                if event.buttons[2]:
                    # clicked on right button and moving
                    position = pygame.mouse.get_pos()
                    rel = event.rel
                    self.change_nodes_pos(rel[0], rel[1])
                if event.buttons[0]:
                    # clicked on left button to drag node
                    position = pygame.mouse.get_pos()
                    node = self.selected_node(position)
                    if node != None:
                        rel = event.rel
                        self.change_node_pos(node, rel[0], rel[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                # if left button is clicked
                position = pygame.mouse.get_pos()
                node = self.selected_node(position)
                if node != None:
                    self.cache_enqueue_selected_nodes(node)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # if clicked on Button Menu
                if self.button_menu.box.collidepoint(event.pos):
                    self.button_menu.clicked()
                    self.switch_to_menu()

    def refresh(self):
        while 1:
            self.keys_listener_selected()
            self.draw_screen_selected()
