import pygame as p
import copy

class Cell:
    #row and col start with index 0
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value

        #sector takes the form "xy" where x is row and y is col
        self.sector = str((row // 3) + 1) + str((col // 3) + 1)

        self.pos_values = []
    
    #repr method used to print value when cell object is displayed
    def __repr__(self):
        return str(self.value)

    #for explicitly setting values
    def set_value(self, value):
        self.value = value

    #for adding possible values
    def add_pos_value(self, value):
        if value not in self.pos_values:
            self.pos_values.append(value)

            #to make it easier we sort the list of possible values
            self.pos_values.sort()
    
    #to easily remove possible values from the list
    def remove_pos_value(self, value):
        if value in self.pos_values:
            self.pos_values.remove(value)

            #to make it easier we sort the list of possible values
            self.pos_values.sort()

class Game_Grid:
    def __init__(self):
        self.current_game_grid = [[None] * 9] * 9
        for i in range(9):
            for j in range(9):
                self.current_game_grid[i][j] = Cell(i, j, i)
                print(f"value of current cell is {self.current_game_grid[i][j]}")
                print(f"value of first cell is {self.current_game_grid[0][0]}")

# test_grid = Game_Grid()
# print(test_grid.current_game_grid)

list1 = [[0] * 9] * 9

for i in range(9):
    for j in range(9):
        list1[i][j] = j
        print(f"current list element is {list1[i][j]}")
        print(f"first list element is {list1[0][0]}")

print(list1)