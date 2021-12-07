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


def order(x, y):
    """
    функция принимает на вход  х и у номера узла и возвращает номер узла в матрице смежности
    :return:
    """
    return x * 5 + y


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

adjacency_matrix = numpy.zeros((25, 25))

clock = pygame.time.Clock()
clock.tick(FPS)
finished = False

while not finished:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if (pygame.mouse.get_pos()[0] >= 600) and (pygame.mouse.get_pos()[0] <= 960) and (
                    pygame.mouse.get_pos()[1] >= 120) and (pygame.mouse.get_pos()[1] <= 480):
                x = (pygame.mouse.get_pos()[0] - 600) / 90
                y = (pygame.mouse.get_pos()[1] - 120) / 90
                x1 = math.floor(x)
                y1 = math.floor(y)
                x2 = math.ceil(x)
                y2 = math.ceil(y)
                if pygame.key.get_pressed()[K_1]:
                    realX = min(x - x1, x2 - x)
                    realY = min(y - y1, y2 - y)

                    if realX >= realY:
                        if abs(y - y1) >= abs(y2 - y):
                            pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y2 * 90),
                                             (600 + x2 * 90, 120 + y2 * 90), 5)

                            adjacency_matrix[order(x1, y2), order(x2, y2)] = 1
                            adjacency_matrix[order(x2, y2), order(x1, y2)] = 1


                        else:
                            pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y1 * 90),
                                             (600 + x2 * 90, 120 + y1 * 90), 5)
                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 1
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 1

                    else:
                        if abs(x - x1) >= abs(x2 - x):
                            pygame.draw.line(screen, (255, 255, 255), (600 + x2 * 90, 120 + y1 * 90),
                                             (600 + x2 * 90, 120 + y2 * 90), 5)
                            adjacency_matrix[order(x2, y1), order(x2, y2)] = 1
                            adjacency_matrix[order(x2, y2), order(x2, y1)] = 1

                        else:
                            pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y1 * 90),
                                             (600 + x1 * 90, 120 + y2 * 90), 5)
                            adjacency_matrix[order(x1, y1), order(x1, y2)] = 1
                            adjacency_matrix[order(x1, y2), order(x1, y1)] = 1

        if event.type == pygame.QUIT:
            finished = True
            print(adjacency_matrix)

        pygame.display.update()

pygame.quit()
