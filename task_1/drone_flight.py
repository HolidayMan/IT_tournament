import pygame
import gui
from gui import fields
from threading import Thread
from math import ceil
from math_functions import Vector, export_cordinates, Point, calculate_move_vector
from map_building import Map
import os

# gui.w_parametrs.mainloop()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128,128,128)
GREEN = (0,128,0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
AMARANT_MAGENTA = (223, 48, 214)
CYAN = (48, 218, 223)


fields.allowed_height = 50
fields.focus_distance = 4
fields.matrix_width = 4
fields.matrix_length = 3
fields.battery_flight_spending = 0.01
fields.battery_photo_spending = 0.2
fields.territory_width = 300
fields.territory_length = 125
fields.battery = 100


class Drone:
    def __init__(self, canvas, cordinates, battery):
        self.canvas = canvas
        self.x = cordinates[0]
        self.y = cordinates[1]
        self.battery = battery

    def construction(self):
            pygame.draw.rect(screen,CYAN, [self.x-5, self.y-5,10, 10], 2)
            pygame.draw.line(screen, CYAN, [self.x-10, self.y-10], [self.x+10, self.y+10], 3)
            pygame.draw.line(screen, CYAN, [self.x-10, self.y+10], [self.x+10, self.y-10], 3)
            for i in range(3):
                pygame.draw.ellipse(screen, AMARANT_MAGENTA, [(self.x-14)-(i*2), (self.y-14)-(i*2), 10+(i*4), 10+(i*4)], 1)
            for i in range(3):
                pygame.draw.ellipse(screen, AMARANT_MAGENTA, [(self.x+7)-(i*2), (self.y+7)-(i*2), 10+(i*4), 10+(i*4)], 1)
            for i in range(3):
                pygame.draw.ellipse(screen, AMARANT_MAGENTA, [(self.x-14)-(i*2), (self.y+7)-(i*2), 10+(i*4), 10+(i*4)], 1)
            for i in range(3):
                pygame.draw.ellipse(screen, AMARANT_MAGENTA, [(self.x+7)-(i*2), (self.y-14)-(i*2), 10+(i*4), 10+(i*4)], 1)


    def move(self, v):
        self.x = ceil(self.x + v.x) if v.x > 0 else int(self.x + v.x)
        self.y = ceil(self.y + v.y) if v.y > 0 else int(self.y + v.y)
        self.battery -= fields.battery_flight_spending * abs(v)


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

L1 = int((A1*h)/F)
L2 = int((A2*h)/F)

PH_P = ceil(l2/L1) # фото на проход
KP = ceil(l1/L2) # кол-во проходов
K_PH = PH_P * KP # кол-во фото

bph_all = K_PH*(bph+bfl) # затраты на фото

x1 = L2/2 + 50
y1 = L1/2 + 50
x2 = x1 + L2*(KP-1)
y2 = y1
x3 = x2
y3 = y1 + L1 * PH_P - L1


s = Vector(x1-base.x, y1-base.y)
e = Vector(base.x-x2, base.y-y2) if KP % 2 == 0 else Vector(base.x-x3, base.y-y3)

l_all = 2*h + abs(s) + L1 * PH_P * KP + L2 * (KP - 1) + abs(e)
bfl_all = l_all * bfl

b_all = bph_all + bfl_all

if b_all > b:
    print('Unreal task')
    exit()

cordinates = [base]

smv, s_dots_amount = calculate_move_vector(s, 10)

cordinates.extend([Point(int(base.x+smv.x*i), int(base.y+smv.y*i), BLACK) for i in range(1, s_dots_amount+1)]) # путь от базы до первой точки

dots_in_the_middle_y = int(L1 / 10)
dots_in_the_middle_x = int(L2/11)


PHOTO_DOTS_COLOR = ORANGE
PATH_DOTS_COLOR = YELLOW
for i in range(KP):
    step = 1 if i % 2 == 0 else -1
    for j in range(0, PH_P*dots_in_the_middle_y-(dots_in_the_middle_y-1), step) if step == 1 else range(PH_P*dots_in_the_middle_y-dots_in_the_middle_y, -1, step):
        cordinates.append(Point(int(x1+L2*i), int(y1+L1/dots_in_the_middle_y*j), PATH_DOTS_COLOR if j % dots_in_the_middle_y != 0 else PHOTO_DOTS_COLOR))
    if i < KP-1:
        j = j if i % 2 == 0 else 0
        for k in range(1, dots_in_the_middle_x):
            cordinates.append(Point(int(x1+L2*i+(L2/dots_in_the_middle_x*k)), int(y1+L1/dots_in_the_middle_y*j), PATH_DOTS_COLOR))


end_point = cordinates[-1]
emv, e_dots_amount = calculate_move_vector(e, 10)
cordinates.extend([Point(int(end_point.x+emv.x*i), int(end_point.y+emv.y*i), RED) for i in range(1, e_dots_amount)]) # путь от последней точки до базы
cordinates.append(base)

export_cordinates(cordinates)

pygame.init()

size = (int(l1 + 50 + 400), int(l2 + 50 + 200))

screen = pygame.display.set_mode(size)
# bg = pygame.image.load("Droneshot.JPG")
 
pygame.display.set_caption("Drone travel")
 
done = False
done2 = False

clock = pygame.time.Clock()

drone = Drone(screen, (base.x, base.y), fields.battery)


pygame.font.init()
comic_sans_font = pygame.font.SysFont('Comic Sans MS', 30)
arial_font = pygame.font.SysFont('Arial', 15)
battery_surface = comic_sans_font.render(str(round(drone.battery, 2)), False, (0, 0, 0))
photo_amount_surface = arial_font.render(f'дрон зробить {K_PH} фото', False, (0, 0, 0))
dron_flight_amount_surface = arial_font.render(f'дрон пролетить {round(l_all, 1)} метрів', False, (0, 0, 0))
battery_amount_surface = arial_font.render(f'дрон витратить {round(b_all, 2)}% заряду', False, (0, 0, 0))
photo_frequency_surface = arial_font.render(f'частота спрацювання затвору: 1/{round(L1, 1)} (фото/метр)', False, (0, 0, 0))



def photo(point: Point):
    return pygame.draw.rect(screen, (230, 230, 230), (point.x-int(L2/2), point.y-int(L1/2), L2, L1))


def draw_battery_rect(surface, battery_start, battery_amount, start_cord, max_width, length):
    if 0 <= battery_amount < 30:
        color = (255, 0, 0)
    elif 30 <= battery_amount < 70:
        color = (255, 255, 0)
    elif 70 <= battery_amount <= 100:
        color = (0, 255, 0)
    l = int(max_width - (max_width-max_width * (battery_amount/100)))
    pygame.draw.rect(surface, color, start_cord+(l, length))


territory_photo = Map((int(l1), int(l2)), (int(L2), int(L1)), 'territory.jpg', 'Droneshot.jpg')
territory_surface = pygame.image.load('territory.jpg')

map_photo = Map((int(l1), int(l2)), (int(L2), int(L1)), 'map.jpg')


points = (point for point in cordinates)
point1 = points.__next__()
point2 = points.__next__()
move = True
dmv, points_in_the_middle = calculate_move_vector(Vector(point2.x - point1.x, point2.y - point1.y), 2)
photographing = False
photo_times = 0

photos_made = 0

takeoff = True
takeofftimes = 0
landing = False
landingtimes = 0

while not done:
    map_surface = pygame.image.load('map.jpg')
    screen.fill(WHITE)
    screen.blit(map_surface, ((l1+150, 200)))
    screen.blit(territory_surface, (50, 50))

    screen.blit(photo_amount_surface, (30, l2+120))
    screen.blit(dron_flight_amount_surface, (30, l2+150))
    screen.blit(battery_amount_surface, (30, l2+180))
    screen.blit(photo_frequency_surface, (30, l2+210))

    pygame.draw.circle(screen, base.color, (base.x, base.y), 4)
    for point in cordinates[1:]:
        pygame.draw.circle(screen, point.color, (point.x, point.y), 4 if point.color == PHOTO_DOTS_COLOR else 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if not done2:
        if takeoff:
            if takeofftimes == 50:
                takeoff = False
                takeofftimes = 0
            drone.battery -= fields.battery_flight_spending
            takeofftimes += 1
        if landing:
            if landingtimes == 50:
                done2 = True
                landing = False
                move = False
                landingtimes = 0
            drone.battery -= fields.battery_flight_spending
            landingtimes += 1
        if move:
            if not photographing:
                if ((dmv.x < 0 and drone.x > point2.x) or (dmv.x > 0 and drone.x < point2.x)) or \
                ((dmv.y < 0 and drone.y > point2.y) or (dmv.y > 0 and drone.y < point2.y)) or \
                ((dmv.x < 0 and drone.x > point2.x and int(drone.x + dmv.x) > point2.x) or \
                (dmv.x > 0 and drone.x < point2.x and int(drone.x + dmv.x) < point2.x)) or \
                ((dmv.y < 0 and drone.y > point2.y and int(drone.y + dmv.y) > point2.y) or (dmv.y > 0 and drone.y < point2.y and int(drone.y + dmv.y) < point2.y)):
                    drone.move(dmv)
                else:
                    if point2 == cordinates[-1]:
                        landing = True
                    else:
                        drone.move(Vector(point2.x - drone.x, point2.y-drone.y))
                        point1 = point2
                        point2 = points.__next__()

                    dmv, points_in_the_middle = calculate_move_vector(Vector(point2.x - point1.x, point2.y - point1.y), 2)
                    if point1.color == PHOTO_DOTS_COLOR:
                        photographing = True
                        drone.battery -= fields.battery_photo_spending
        if photographing:
            if photo_times > 7:
                photos_made += 1
                map_photo.build_image((Point(point1.x, point1.y, BLUE)), territory_photo.get_fragment(Point(point1.x, point1.y, BLUE)))
                photographing = False
                photo_times = 0
            else:
                photo_times+=1
                photo(point1)
    
    drone.construction()

    move = not move

    battery_surface = comic_sans_font.render(f'заряд батареї: {round(drone.battery, 2)}%', False, (0, 0, 0))
    screen.blit(battery_surface, (l1 + 150, 50))
    pygame.draw.rect(screen, BLACK, (l1+148, 78, 227, 53), 2)
    draw_battery_rect(screen, fields.battery, drone.battery, (l1+150, 80), 225, 50)

    photos_made_surface = comic_sans_font.render(f'фото зроблено: {photos_made}', False, (0, 0, 0))
    screen.blit(photos_made_surface, (l1 + 150, 150))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

os.remove('territory.jpg')
os.remove('map.jpg')
