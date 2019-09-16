import pygame
import gui
from gui import fields
from threading import Thread


gui.w_parametrs.mainloop()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128,128,128)
GREEN = (0,128,0)


 
pygame.init()
 
size = (1000, 1000)
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
    pygame.draw.rect(screen,GREY,[490,490,20,20],2)
    pygame.draw.line(screen, GREY, [480,480], [520,520], 5)
    pygame.draw.line(screen, GREY, [480,520], [520,480], 5)
    for i in range(5):
        pygame.draw.ellipse(screen,GREY,[475-(i*2),475-(i*2),10+(i*4),10+(i*4)],1)
    for i in range(5):
        pygame.draw.ellipse(screen,GREY,[515-(i*2),515-(i*2),10+(i*4),10+(i*4)],1)
    for i in range(5):
        pygame.draw.ellipse(screen,GREY,[475-(i*2),515-(i*2),10+(i*4),10+(i*4)],1)
    for i in range(5):
        pygame.draw.ellipse(screen,GREY,[515-(i*2),475-(i*2),10+(i*4),10+(i*4)],1)
    pygame.draw.ellipse(screen, (0,128,0), [425,925,150,49])
    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render("Play", True, BLACK)
    screen.blit(text, [480, 937])

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
