import pygame

from maincode import screen


def knots():
    for i in range(5):
        for j in range(5):
            pygame.draw.circle(screen, (255, 255, 255), (500+i*5, 5*j+20), 2, 0)



