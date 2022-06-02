import pygame as p
import time

p.init()

#arbitrary comment
class Node:
    def __init__(self, is_base_node, x_pos, y_pos, layer, index, parent_nodes = [], is_draw_node = False):

        self.dt = 0.01
        self.is_base_node = is_base_node
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.layer = layer
        self.index = index
        self.is_draw_node = is_draw_node
        self.is_moving = False

        self.parent_nodes = parent_nodes
        self.child_nodes = []
    
    def update_current(self):
        self.x_current = (self.x_end - self.x_start) // 2
        self.y_current = (self.y_end - self.y_start) // 2
    
    def display_node(self, screen):
        if self.is_draw_node:
            p.draw.circle(screen, (255, 0, 0), (node.x_pos, node.y_pos), 5)
        else:
            p.draw.circle(screen, (0, 0, 255), (node.x_pos, node.y_pos), 5)
    
def create_children_nodes(nodes, layer, global_node_list):
    if len(nodes) <= 1:
        return
    children_nodes = []
    index = 0
    for i in range(len(nodes)):
        if i < len(nodes) - 1:
            new_node = Node(False, nodes[i].x_pos, nodes[i].y_pos, layer, index, [nodes[i], nodes[i + 1]])
            index += 1
            nodes[i].child_nodes.append(new_node)
            nodes[i + 1].child_nodes.append(new_node)
            
            children_nodes.append(new_node)

    if len(children_nodes) == 1:
        children_nodes[0].is_draw_node = True

    global_node_list.append(children_nodes)
    create_children_nodes(children_nodes, layer + 1, global_node_list)



screen = p.display.set_mode([1300, 750])

running = True

in_main_state = False

nodes = []

while running:

    in_setup = True

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    screen.fill((255, 255, 255))

    p.display.update()

    base_nodes = []
    index = 0
    layer = 0

    while in_setup:
        for event in p.event.get():

            if event.type == p.MOUSEBUTTONDOWN:
                position = p.mouse.get_pos()
                x_pos = position[0]
                y_pos = position[1]

                p.draw.circle(screen, (0, 0, 0), (x_pos, y_pos), 10)

                base_node = Node(True, x_pos, y_pos, layer, index)
                index += 1
                base_nodes.append(base_node)

                p.display.update()
            
            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE and len(base_nodes) > 1:
                    in_setup = False
                    in_main_state = True
            
            if event.type == p.QUIT:
                running = False
                in_setup = False
    
    nodes.append(base_nodes)


    for i in range(len(nodes[0])):
        create_children_nodes(nodes[-1], i + 1, nodes)
    
    
    p.display.update()

    while in_main_state:
        for event in p.event.get():
            if event.type == p.QUIT:
                in_main_state = False
                running = False
            
            for node_layer in nodes:
                for node in node_layer:
                    if not node.is_base_node:
                        parent_node_1 = node.parent_nodes[0]
                        parent_node_2 = node.parent_nodes[1]
                        node.x_pos = (parent_node_1.x_pos + parent_node_2.x_pos) // 2
                        node.y_pos = (parent_node_1.y_pos + parent_node_2.y_pos) // 2

                        x_vector = (parent_node_2.x_pos - parent_node_1.x_pos)
                        y_vector = (parent_node_2.y_pos - parent_node_1.y_pos)

                        node.display_node(screen)

                        x = parent_node_1.x_pos
                        y = parent_node_1.y_pos

                        p.draw.line(screen, (255, 0, 255), (x, y), (x + x_vector, y + y_vector))

            p.display.update()
            
            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE:
                    in_main_state = False

    #new code for moving circles

    path = []

    time_passed = 0
    dt = 0.01 

    while time_passed <= 1:

        for event in p.event.get():
            if event.type == p.QUIT:
                time_passed = 2

        screen.fill((255, 255, 255))

        for node in nodes[0]:
            p.draw.circle(screen, (0, 0, 0), (node.x_pos, node.y_pos), 10)

        for i in range(len(path)):
            coordinate = path[i]
            p.draw.circle(screen, (255, 0, 0), (coordinate[0], coordinate[1]), 5)
            if i < len(path) - 1:
                p.draw.line(screen, (255, 0, 0), (coordinate[0], coordinate[1]), (path[i + 1][0], path[i + 1][1]))

        for node_layer in nodes:
            for node in node_layer:
                if not node.is_base_node:
                    parent_node_1 = node.parent_nodes[0]
                    parent_node_2 = node.parent_nodes[1]

                    x_vector = (parent_node_2.x_pos - parent_node_1.x_pos)
                    y_vector = (parent_node_2.y_pos - parent_node_1.y_pos)

                    x = parent_node_1.x_pos
                    y = parent_node_1.y_pos

                    node.x_pos = x + x_vector * time_passed
                    node.y_pos = y + y_vector * time_passed

                    node.display_node(screen)

                    p.draw.line(screen, (255, 0, 255), (x, y), (x + x_vector, y + y_vector))
                    
                    p.display.update()

                    if node.is_draw_node:
                        new_coordinate = [node.x_pos, node.y_pos]
                        path.append(new_coordinate)
        time_passed += dt
    in_game_end = True

    screen.fill((255, 255, 255))

    for i in range(len(path)):
        coordinate = path[i]
        p.draw.circle(screen, (255, 0, 0), (coordinate[0], coordinate[1]), 5)
        if i < len(path) - 1:
            p.draw.line(screen, (255, 0, 0), (coordinate[0], coordinate[1]), (path[i + 1][0], path[i + 1][1]))
    p.display.update()


    while in_game_end:
        for event in p.event.get():
            if event.type == p.QUIT:
                quit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE:
                    in_game_end = False
    
    nodes = []
    path = []
