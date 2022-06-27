from numpy import square
import pygame as p
from pyparsing import with_attribute
from class_file import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 190, 200)


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

#make every cell have every digit as a possible value, or none if the cell already has a value
def reset_pos_values(board):
    for i in range (9):
        for j in range(9):
            if board.current_game_grid[i][j].value == None:
                board.current_game_grid[i][j].pos_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for k in range(1, 10):
                    if k in board.current_game_grid[i][j].blacklisted_values:
                        board.current_game_grid[i][j].pos_values.remove(k)
            else:
                board.current_game_grid[i][j].pos_values = []

#make it so that all solved cells have an empty pos_values list
def update_solved_cells(board):
    for cell_row in board.current_game_grid:
        for cell in cell_row:
            if cell.value:
                cell.pos_values = []

#draws a square at the specified row and col with a specified color
def draw_square(row, col, color):
    new_coordinates = index_to_coordinates(row, col)

    #test validity of row and col
    rect_x_start = new_coordinates[0] + 1
    rect_y_start = new_coordinates[1] + 1

    #draw square where user clicked
    coordinates_square = (rect_x_start + 2, rect_y_start + 2, 75, 75)
    p.draw.rect(screen, color, p.Rect(coordinates_square))

def remove_non_digit_values_and_0s(board):
    for cell_row in board.current_game_grid:
        for cell in cell_row:
            if cell.value and ((not str(cell.value).isdigit()) or cell.value == 0):
                cell.value = None

            if cell.value:
                cell.value = int(str(cell.value))

#draws every cell's value on the board where the cell is located
def draw_cell_values(board):
    for cell_row in board.current_game_grid:
        for cell in cell_row:
            if cell.value:
                number = font.render(str(cell.value), True, BLACK)
                number_box = number.get_rect()

                coordinates = index_to_coordinates(cell.row, cell.col)

                x_location = coordinates[0] + 39
                y_location = coordinates[1] + 39

                number_box.center = (x_location , y_location)

                if cell.computer_generated:
                    draw_square(cell.row, cell.col, PINK)

                screen.blit(number, number_box)
def draw_grid():
    #draw grid
    for i in range(10):
        p.draw.line(screen, BLACK, (i * 80 + 10, 10), (i * 80 + 10, 730))
        if (i % 3 == 0):
            p.draw.line(screen, BLACK, (i * 80 + 10, 10), (i * 80 + 10, 730), width=6)
    for i in range(10):
        p.draw.line(screen, BLACK, (10, i * 80 + 10), (730, i * 80 + 10))
        if (i % 3 == 0):
            p.draw.line(screen, BLACK, (10, i * 80 + 10), (730, i * 80 + 10), width=6)

def find_cell_values_row(board, cell):
    pos_values_for_row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for num in cell.blacklisted_values:
        pos_values_for_row.remove(num)

    for i in range(9):
        value = board.current_game_grid[cell.row][i].value
        if value in pos_values_for_row:
            pos_values_for_row.remove(value)
    
    for num in cell.pos_values:
        if num not in pos_values_for_row:
            cell.pos_values.remove(num)

    

def find_cell_values_col(board, cell):
    pos_values_for_col = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for num in cell.blacklisted_values:
        pos_values_for_col.remove(num)
        
    for i in range(9):
        value = board.current_game_grid[i][cell.col].value
        if value in pos_values_for_col:
            pos_values_for_col.remove(value)
    
    for num in cell.pos_values:
        if num not in pos_values_for_col:
            cell.pos_values.remove(num)



def find_cell_values_sector(board, cell):
    pos_values_for_sector = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for num in cell.blacklisted_values:
        pos_values_for_sector.remove(num)
        
    row = (cell.row // 3) * 3
    col = (cell.col // 3) * 3
    for i in range(row, row + 3):
        for j in range(col, col + 3):
            value = board.current_game_grid[i][j].value
            if value in pos_values_for_sector:
                pos_values_for_sector.remove(value)
    
    for num in cell.pos_values:
        if num not in pos_values_for_sector:
            cell.pos_values.remove(num)

def find_pos_values_for_cell(board, cell):
    find_cell_values_row(board, cell)
    find_cell_values_col(board, cell)
    find_cell_values_sector(board, cell)

#find the possible values for cells based on the row they're in
def find_values_with_row(board, row):
    pos_values_for_row = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        value = board.current_game_grid[row][i].value
        if value and int(value) in pos_values_for_row:
            value = int(value)
            pos_values_for_row.remove(value)

    for i in range(1, 10):  #iterates through the values to be in possible values
        for j in range(9): #iterate through the cells
            current_cell_pv = board.current_game_grid[row][j].pos_values #possible values for current cell
            if (i not in pos_values_for_row) and (i in current_cell_pv):
                board.current_game_grid[row][j].pos_values.remove(i)

#find the possible values for cells based on the row they're in
def find_values_with_col(board, col):
    pos_values_for_col = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        value = board.current_game_grid[i][col].value
        if value and (int(value) in pos_values_for_col):
            value = int(value)
            pos_values_for_col.remove(value)

    for i in range(1, 10):  #iterates through the values to be in possible values
        for j in range(9): #iterate through the cells
            current_cell_pv = board.current_game_grid[j][col].pos_values #possible values for current cell
            if i not in pos_values_for_col and (i in current_cell_pv):
                board.current_game_grid[j][col].pos_values.remove(i)

#find the possible values for cells based on the sector they're in
def find_values_with_sector(board, sector):
    pos_values_for_sector = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    start_row = (int(sector[0]) - 1) * 3
    start_col = (int(sector[1]) - 1) * 3

    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            value = board.current_game_grid[i][j].value
            if value and (int(value) in pos_values_for_sector):
                value = int(value)
                pos_values_for_sector.remove(value)

    for i in range(1, 10): #iterate through the values to be in possible values
        for j in range(start_row, start_row + 3): #iterate through rows of sector
            for k in range(start_col, start_col + 3): #iterate through columns of sector
                current_cell_pv = board.current_game_grid[j][k].pos_values #possible values for current cell
                if i not in pos_values_for_sector and (i in current_cell_pv):
                    board.current_game_grid[j][k].pos_values.remove(i)

#add the possible values for each cell to each cells possible values attribute
def find_possible_cell_values(board):
    reset_pos_values(board)

    for row in range(9):
        find_values_with_row(board, row)

    for col in range(9):
        find_values_with_col(board, col)
        
    for cell_row in board.current_game_grid:
        for cell in cell_row:
            find_values_with_sector(board, cell.sector)

def find_possible_cell_values_v2(board):
    for cell_row in board.current_game_grid:
            for cell in cell_row:
                if cell.value == None:
                    cell.pos_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                find_pos_values_for_cell(board, cell)

#game loop
board = Board()
font = p.font.SysFont("arial", 80)
while True:
    #while in the phase where the user puts numbers into the grid
    square_selected = "00"
    while in_input_phase:
        for event in p.event.get():
            
            if event.type == p.QUIT:
                p.quit()
            
            if event.type == p.KEYDOWN and event.key == p.K_s:
                print(board.current_game_grid[0][0].value)

            if event.type == p.KEYDOWN and event.key == p.K_LEFT and int(square_selected[1]) > 0:
                square_selected = square_selected[0] + str(int(square_selected[1]) - 1)
                draw_grid()
                draw_cell_values(board)

            if event.type == p.KEYDOWN and event.key == p.K_RIGHT and int(square_selected[1]) < 8:
                square_selected = square_selected[0] + str(int(square_selected[1]) + 1)
                draw_grid()
                draw_cell_values(board)

            if event.type == p.KEYDOWN and event.key == p.K_UP and int(square_selected[0]) > 0:
                square_selected = str(int(square_selected[0]) - 1) + square_selected[1]
                draw_grid()
                draw_cell_values(board)

            if event.type == p.KEYDOWN and event.key == p.K_DOWN and int(square_selected[0]) < 8:
                square_selected = str(int(square_selected[0]) + 1) + square_selected[1]
                draw_grid()
                draw_cell_values(board)

            if event.type == p.KEYDOWN and event.key == p.K_t:
                print("initiate testing")

                square_selected = None

                #row 0
                values = [None, 6, 9, None, None, None, None, 7, 8]
                for i in range(9):
                    board.current_game_grid[0][i].value = values[i]
                
                #row_1
                values = [5, None, None, None, 4, None, None, None, None]
                for i in range(9):
                    board.current_game_grid[1][i].value = values[i]
                
                #row_2
                values = [None, None, None, None, None, 7, 6, None, 5]
                for i in range(9):
                    board.current_game_grid[2][i].value = values[i]
                
                #row_3
                values = [9, 4, 2, 7, None, 3, 1, 5, 6]
                for i in range(9):
                    board.current_game_grid[3][i].value = values[i]
                
                #row_4
                values = [7, None, 6, 5, None, 2, 8, 4, 3]
                for i in range(9):
                    board.current_game_grid[4][i].value = values[i]
                
                #row_5
                values = [None, None, None, 1, None, 4, None, 9, None]
                for i in range(9):
                    board.current_game_grid[5][i].value = values[i]
                
                #row_6
                values = [None, None, None, None, None, 6, None, 8, None]
                for i in range(9):
                    board.current_game_grid[6][i].value = values[i]
                
                #row_7
                values = [6, None, 1, None, 3, 9, None, None, None]
                for i in range(9):
                    board.current_game_grid[7][i].value = values[i]
                
                #row_8
                values = [None, 5, 4, None, 7, None, 3, None, None]
                for i in range(9):
                    board.current_game_grid[8][i].value = values[i]

            draw_cell_values(board)

            remove_non_digit_values_and_0s(board)
            draw_grid()
            
            #make sure the selected square is always green
            if square_selected:
                row = int(square_selected[0])
                col = int(square_selected[1])
                draw_square(row, col, GREEN)
                draw_cell_values(board)

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
            if (square_selected and event.type == p.KEYDOWN and not 
            event.key == p.K_SPACE):
                screen.fill(WHITE)

                key = event.unicode
                
                row = int(square_selected[0])
                col = int(square_selected[1])

                if not (event.key in [p.K_LEFT, p.K_RIGHT, p.K_DOWN, p.K_UP]):
                    board.current_game_grid[row][col].value = key

                draw_cell_values(board)
            
            if event.type == p.KEYDOWN and event.key == p.K_SPACE:
                in_input_phase = False
                in_solving_phase = True

                draw_cell_values(board)

                p.display.update()

                remove_non_digit_values_and_0s(board)
            
        
        draw_cell_values(board)

        p.display.update()
    

    remove_non_digit_values_and_0s(board)

    for cell_row in board.current_game_grid:
        for cell in cell_row:
            if cell.value:
                cell.value = int(cell.value)

    definite_value_found = True #becomes false if no definite value can be found
    current_game_state_faulty = False
    num_solved = 0 #number of cells with a definite value
    
    while in_solving_phase:
        num_solved = 0

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
        
        # find_possible_cell_values(board)

        find_possible_cell_values_v2(board)

        definite_value_found = False

        #fills out values with definite solution
        for cell_row in board.current_game_grid:
            for cell in cell_row:
                find_pos_values_for_cell(board, cell)
                if cell.value:
                    num_solved += 1
                
                if len(cell.pos_values) == 0 and not cell.value:
                    current_game_state_faulty = True
                elif len(cell.pos_values) == 1:
                    cell.value = cell.pos_values[0]
                    cell.computer_generated = True
                    cell.pos_values = []
                    definite_value_found = True
        
        if num_solved >= 81:
            in_solving_phase = False
            in_end_phase = True
            print("we're in the endgame now")
            

        #chooses value for cell with few solutions if no definite solution exists
        if definite_value_found == False and (not current_game_state_faulty) and (not in_end_phase):
            minimum_PV_length = 9
            nexus_cell_row = None
            nexus_cell_col = None
            for cell_row in board.current_game_grid:
                for cell in cell_row:
                    find_pos_values_for_cell(board, cell)
                    if len(cell.pos_values) <= minimum_PV_length and cell.value == None:
                        minimum_PV_length = len(cell.pos_values)
                        nexus_cell_row = cell.row
                        nexus_cell_col = cell.col

            archived_game_grid = copy.deepcopy(board.current_game_grid)

            board.previous_game_grids.append(archived_game_grid)

            board.nexus_cell_log.append((nexus_cell_row, nexus_cell_col))
            
            nexus_cell_value = board.current_game_grid[nexus_cell_row][nexus_cell_col].pos_values[0]
            
            board.current_game_grid[nexus_cell_row][nexus_cell_col].value = nexus_cell_value

            board.current_game_grid[nexus_cell_row][nexus_cell_col].computer_generated = True

            print(f"""\nadding nexus cell coordinates {nexus_cell_row}-{nexus_cell_col} to nexus_cell_log
             and giving cell {nexus_cell_row}-{nexus_cell_col} a value of 
             {nexus_cell_value}\n""")

            update_solved_cells(board)

            # find_possible_cell_values(board)
            find_possible_cell_values_v2(board)

            definite_value_found = True

        #restores previous gamestate with one possible value removed if current grid is faulty
        if current_game_state_faulty and not in_end_phase:

            nexus_cell_coordinates = board.nexus_cell_log.pop()

            nexus_cell_row = nexus_cell_coordinates[0]
            nexus_cell_col = nexus_cell_coordinates[1]

            faulty_value = board.current_game_grid[nexus_cell_row][nexus_cell_col].value

            board.current_game_grid = board.previous_game_grids.pop()

            board.nexus_cell = board.current_game_grid[nexus_cell_row][nexus_cell_col]

            board.nexus_cell.blacklisted_values.append(faulty_value)
            
            print(f"""\nnexus cell {nexus_cell_row}-{nexus_cell_col} had a value of {faulty_value} 
            which was wrong. blacklisting {faulty_value} from cell {nexus_cell_row}-{nexus_cell_col}\n""")

            current_game_state_faulty = False

            # find_possible_cell_values(board)
            find_possible_cell_values_v2(board)

        screen.fill(WHITE)
        draw_grid()
        draw_cell_values(board)
        p.display.update()
    
    screen.fill(YELLOW)
    draw_grid()
    draw_cell_values(board)
    p.display.update()

    while in_end_phase:

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
        

            
