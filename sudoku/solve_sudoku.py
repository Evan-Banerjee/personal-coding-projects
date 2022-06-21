import pygame as p

WHITE = (255, 255, 255)

p.init()
screen = p.display.set_mode((720, 720))
screen.fill(WHITE)
p.display.set_caption("sudoku solver")
running = True

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
    p.display.update()
