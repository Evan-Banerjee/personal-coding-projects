import pygame as p
from pyparsing import with_attribute
from class_file import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

#pygame setup
p.init()
screen = p.display.set_mode((740, 740))
screen.fill(WHITE)
p.display.set_caption("sudoku solver")

#different game phases
in_input_phase = True
in_solving_phase = False
in_end_phase = False

#takes in coordinates and returns index of square coordinates are in
def coordinates_to_index(x_pos, y_pos):
    col = (x_pos - 10) // 80
    row = (y_pos - 10) // 80
    return [row, col]

#takes in the index of where a square is and returns the coordinates of the top left corner of the square
def index_to_coordinates(row, col):
    x_coordinate = col * 80 + 10
    y_coordinate = row * 80 + 10
    return [x_coordinate, y_coordinate]

#draws a square at the specified row and col with a specified color
def draw_square(row, col, color):
    new_coordinates = index_to_coordinates(row, col)

    #test validity of row and col
    rect_x_start = new_coordinates[0] + 1
    rect_y_start = new_coordinates[1] + 1

    #draw square where user clicked
    coordinates_square = (rect_x_start + 2, rect_y_start + 2, 75, 75)
    p.draw.rect(screen, color, p.Rect(coordinates_square))

#draws every cell's value on the board where the cell is located
def draw_cell_values():
    for cell_row in board.current_game_grid:
        for cell in cell_row:
            if cell.value:
                if cell.value[0].isdigit():
                    number = font.render(cell.value, True, BLACK)
                    number_box = number.get_rect()

                    coordinates = index_to_coordinates(cell.row, cell.col)

                    x_location = coordinates[0] + 39
                    y_location = coordinates[1] + 39

                    number_box.center = (x_location , y_location)

                    screen.blit(number, number_box)

#game loop
board = Board()
font = p.font.SysFont("arial", 80)
while True:
    #while in the phase where the user puts numbers into the grid
    square_selected = ""
    while in_input_phase:
        for event in p.event.get():
            
            if event.type == p.QUIT:
                p.quit()

            #draw grid
            for i in range(10):
                p.draw.line(screen, BLACK, (i * 80 + 10, 10), (i * 80 + 10, 730))
                if (i % 3 == 0):
                    p.draw.line(screen, BLACK, (i * 80 + 10, 10), (i * 80 + 10, 730), width=6)
            for i in range(10):
                p.draw.line(screen, BLACK, (10, i * 80 + 10), (730, i * 80 + 10))
                if (i % 3 == 0):
                    p.draw.line(screen, BLACK, (10, i * 80 + 10), (730, i * 80 + 10), width=6)
            
            #make sure the selected square is always green
            if square_selected:
                row = int(square_selected[0])
                col = int(square_selected[1])
                draw_square(row, col, GREEN)

            #find row and col where user clicked
            if event.type == p.MOUSEBUTTONUP:
                
                if square_selected:
                    old_row = int(square_selected[0])
                    old_col = int(square_selected[1])

                    draw_square(old_row, old_col, WHITE)

                coordinates = p.mouse.get_pos()
                index = coordinates_to_index(coordinates[0], coordinates[1])
                row = index[0]
                col = index[1]

                draw_square(row, col, GREEN)

                square_selected = str(row) + str(col)

            #adds the user inputed value to the boards game_grid attribute
            if square_selected and event.type == p.KEYDOWN:
                screen.fill(WHITE)

                key = event.unicode

                if event.type == p.K_BACKSPACE:
                    key = None
                
                row = int(square_selected[0])
                col = int(square_selected[1])
                board.current_game_grid[row][col].value = key

                print("adding " + str(key) + " to a cell")
        
        draw_cell_values()

        p.display.update()
