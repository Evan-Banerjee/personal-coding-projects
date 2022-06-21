import pygame as p

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
    return (row, col)

#takes in the index of where a square is and returns the coordinates of the top left corner of the square
def index_to_coordinates(row, col):
    x_coordinate = col * 80 + 10
    y_coordinate = row * 80 + 10
    return (x_coordinate, y_coordinate)

#game loop
while True:
    #while in the phase where the user puts numbers into the grid
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

            #find row and col where user clicked
            if event.type == p.MOUSEBUTTONUP:
                coordinates = p.mouse.get_pos()
                index = coordinates_to_index(coordinates[0], coordinates[1])
                row = index[0]
                col = index[1]

                new_coordinates = index_to_coordinates(row, col)

                #test validity of row and col
                rect_x_start = new_coordinates[0] + 1
                rect_y_start = new_coordinates[1] + 1

                #draw square where user clicked
                coordinates_square = (rect_x_start, rect_y_start, 79, 79)
                p.draw.rect(screen, GREEN, p.Rect(coordinates_square),)

        p.display.update()
