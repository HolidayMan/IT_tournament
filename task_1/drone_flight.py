import pygame
import gui
from gui import fields
from threading import Thread
from math import ceil
from math_functions import Vector, export_coordinates
from collections import namedtuple

# gui.w_parametrs.mainloop()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128,128,128)
GREEN = (0,128,0)
BLUE = (0, 0, 255)

fields.allowed_height = 50
fields.focus_distance = 4
fields.matrix_width = 4
fields.matrix_length = 3
fields.battery_flight_spending = 0.01
fields.battery_photo_spending = 0.2
fields.territory_width = 200
fields.territory_length = 500
fields.battery = 100

Point = namedtuple('Point', ['x', 'y', 'color'])

base = Point(50, 50, GREY)

l1 = min(fields.territory_length, fields.territory_width)
l2 = max(fields.territory_length, fields.territory_width)


h = fields.allowed_height
F = fields.focus_distance
A1 = min(fields.matrix_width, fields.matrix_length) # геометрия
A2 = max(fields.matrix_width, fields.matrix_length) # матрицы

b = fields.battery 
bph = fields.battery_photo_spending # затраты на фото
bfl = fields.battery_flight_spending # затраты на полет

L1 = (A1*h)/F
L2 = (A2*h)/F

PH_P = ceil(l2/L1) # фото на проход
KP = ceil(l1/L2) # кол-во проходов
K_PH = PH_P * KP # кол-во фото

bph_all = K_PH*(bph+bfl) # затраты на фото

x1 = L2/2 + base.x
y1 = L1/2 + base.y
x2 = x1 + L2*(KP-1)
y2 = y1
x3 = x2
y3 = y1 + L1 * PH_P



s = Vector(x1-base.x, y1-base.y)
e = Vector(base.x-x2, base.y-y2) if KP % 2 == 0 else Vector(base.x-x3, base.y-y3)

l_all = 2*h + abs(s) + L1 * PH_P * KP + L2 * (KP - 1) + abs(e)
bfl_all = l_all * bfl

b_all = bph_all + bfl_all


if b_all > b:
    print('Unreal task')
    exit()

coordinates = []

coordinates.append(base)

for i in range(KP):
    for j in range(PH_P*2-1):
        coordinates.append(Point(int(x1+L2*i), int(y1+L1/2*j), RED if j % 2 == 1 else BLUE))
    if i < KP-1:
        j = j if i % 2 == 0 else 0
        for k in range(1, 3):
            coordinates.append(Point(int(x1+L2*i+(L2/3*k)), int(y1+L1/2*j), RED))



pygame.init()

size = (int(l1 + base.x + 300), int(l2 + base.y + 200))

screen = pygame.display.set_mode(size)
# bg = pygame.image.load("Droneshot.JPG")

 
pygame.display.set_caption("Drone travel")
 
done = False
done2 = False
done3 = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 

while not done:
    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 255, 0 ), (int(base.x), int(base.y), int(l1), int(l2)))
    pygame.draw.circle(screen, base.color, (base.x, base.y), 4)
    for point in coordinates[1:]:
        pygame.draw.circle(screen, point.color, (point.x, point.y), 2)
    # screen.blit(bg(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x=pos[0]
            y=pos[1]
            if 425<x<575 and 425<y<475:
                done2 = True
    # pygame.draw.rect(screen,GREY,[490,490,20,20],2)
    # pygame.draw.line(screen, GREY, [480,480], [520,520], 5)
    # pygame.draw.line(screen, GREY, [480,520], [520,480], 5)
    # for i in range(5):
    #     pygame.draw.ellipse(screen,GREY,[475-(i*2),475-(i*2),10+(i*4),10+(i*4)],1)
    # for i in range(5):
    #     pygame.draw.ellipse(screen,GREY,[515-(i*2),515-(i*2),10+(i*4),10+(i*4)],1)
    # for i in range(5):
    #     pygame.draw.ellipse(screen,GREY,[475-(i*2),515-(i*2),10+(i*4),10+(i*4)],1)
    # for i in range(5):
    #     pygame.draw.ellipse(screen,GREY,[515-(i*2),475-(i*2),10+(i*4),10+(i*4)],1)
    # pygame.draw.ellipse(screen, (0,128,0), [425,925,150,49])
    # font = pygame.font.SysFont('Calibri', 25, True, False)
    # text = font.render("Play", True, BLACK)
    # screen.blit(text, [480, 937])

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
