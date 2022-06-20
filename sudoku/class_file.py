import pygame as p
import copy

class Cell:
    #row and col start with index 0
    def __init__(self, row, col, sector):
        self.row = row
        self.col = col

        #sector takes the form "xy" where x is row and y is col
        self.sector = str((row // 3) + 1) + str((col // 3) + 1)

        self.value = None
        self.pos_values = []

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
        pass
