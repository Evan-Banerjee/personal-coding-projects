import pygame as p
import copy

class Cell:
    #row and col start with index 0
    def __init__(self, row, col, value=None):
        self.row = row
        self.col = col
        self.value = value
        
        self.blacklisted_values = []

        self.computer_generated = False

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

class Board:
    def __init__(self):
        #makes the current game_grid, which is a 2d (9 by 9) array of None objects
        self.current_game_grid = [[None for x in range(9)] for y in range(9)]
        self.previous_game_grids = []
        self.nexus_cell_log = []
        self.nexus_cell = None

        #populates the game_grid with Cell objects
        for i in range(9):
            for j in range(9):
                self.current_game_grid[i][j] = Cell(i, j)

