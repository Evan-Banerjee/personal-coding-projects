class Cell:
    #row and col start with index 0
    def __init__(self, row, col, sector):
        self.row = row
        self.col = col

        #sector takes the form "xy" where x is row and y is col
        self.sector = str((row // 3) + 1) + str((col // 3) + 1)
        
        self.value = None
        self.pos_values = []