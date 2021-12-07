# инициализация экрана, настройка частоты обновления, подключение библиотек
import pygame
import numpy
import math
from random import randint

from pygame import K_1

from grid import *

pygame.init()
FPS = 25
screen = pygame.display.set_mode((1000, 600))


def knots():
    """
    отрисовка узлов схемы, также отдельно в конце отрисовывается плюс и минус батарейки
    :return:
    """
    for i in range(5):
        for j in range(5):
            pygame.draw.circle(screen, (255, 255, 255), (600 + i * 90, 90 * j + 120), 5, 0)

    pygame.draw.circle(screen, (255, 0, 0), (600, 120), 5, 0)
    pygame.draw.circle(screen, (0, 0, 255), (600, 480), 5, 0)


knots()

a = numpy.zeros((25, 25))

clock = pygame.time.Clock()
clock.tick(FPS)
finished = False

while not finished:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if pygame.mouse.get_pos()[0] >= 500:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                x1 = math.floor((x - 600) / 90)
                y1 = math.floor((y - 120) / 90)
                x2 = math.ceil((x - 600) / 90)
                y2 = math.ceil((y - 120) / 90)
                if pygame.key.get_pressed()[K_1]:
                    realX = min((x - 600) / 90 - x1, x2 - (x - 600) / 90)
                    realY = min((y - 120) / 90 - y1, y2 - (y - 120) / 90)
                    print(realX, realY)
                    if realX >= realY:
                        if (y - y1) >= (y2 - y):
                            pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y2 * 90),
                                             (600 + x2 * 90, 120 + y2 * 90), 5)
                        else:
                            pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y1 * 90),
                                             (600 + x2 * 90, 120 + y1 * 90), 5)
                    else:
                        if (x - x1) >= (x2 - x):
                            pygame.draw.line(screen, (255, 255, 255), (600 + x2 * 90, 120 + y1 * 90),
                                             (600 + x2 * 90, 120 + y2 * 90), 5)
                        else:
                            pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y1 * 90),
                                             (600 + x1 * 90, 120 + y2 * 90), 5)

        if event.type == pygame.QUIT:
            finished = True

        pygame.display.update()

pygame.quit()
