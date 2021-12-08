# инициализация экрана, настройка частоты обновления, подключение библиотек
import pygame
import numpy
import math
from random import randint

from pygame import K_1
from pygame import K_2



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


def draw_resist(x1, y1, x2, y2):
    X = 600 + x1 * 90
    Y = 120 + y1 * 90
    XX = 600 + x2 * 90
    YY = 120 + y2 * 90
    XA = (XX + 2 * X) / 3
    YA = (YY + 2 * Y) / 3
    XB = (2 * XX + X) / 3
    YB = (2 * YY + Y) / 3
    if Y == YY:
        WY1 = YA - abs(XX - X) / 9
        WX1 = XA
        WY2 = YA + abs(XX - X) / 9
        WX2 = XA
        ZY1 = YB - abs(XX - X) / 9
        ZX1 = XB
        ZY2 = YB + abs(XX - X) / 9
        ZX2 = XB
    else:
        WY1 = YA
        WX1 = XA - abs(YY - Y) / 9
        WY2 = YA
        WX2 = XA + abs(YY - Y) / 9
        ZY1 = YB
        ZX1 = XB - abs(YY - Y) / 9
        ZY2 = YB
        ZX2 = XB + abs(YY - Y) / 9

    pygame.draw.line(screen, (0, 255, 255), (X, Y), (XA, YA), 5)
    pygame.draw.line(screen, (0, 255, 255), (XB, YB), (XX, YY), 5)
    pygame.draw.line(screen, (0, 255, 255), (WX1, WY1), (WX2, WY2), 5)
    pygame.draw.line(screen, (0, 255, 255), (WX1, WY1), (ZX1, ZY1), 5)
    pygame.draw.line(screen, (0, 255, 255), (ZX1, ZY1), (ZX2, ZY2), 5)
    pygame.draw.line(screen, (0, 255, 255), (WX2, WY2), (ZX2, ZY2), 5)


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
                if pygame.key.get_pressed()[K_2]:
                    realX = min(x - x1, x2 - x)
                    realY = min(y - y1, y2 - y)

                    if realX >= realY:
                        if abs(y - y1) >= abs(y2 - y):
                            draw_resist(x1, y2, x2, y2)

                            adjacency_matrix[order(x1, y2), order(x2, y2)] = 2
                            adjacency_matrix[order(x2, y2), order(x1, y2)] = 2


                        else:
                            draw_resist(x1, y1, x2, y1)

                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 2
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 2

                    else:
                        if abs(x - x1) >= abs(x2 - x):
                            draw_resist(x2, y1, x2, y2)

                            adjacency_matrix[order(x2, y1), order(x2, y2)] = 2
                            adjacency_matrix[order(x2, y2), order(x2, y1)] = 2

                        else:
                            draw_resist(x1, y1, x1, y2)

                            adjacency_matrix[order(x1, y1), order(x1, y2)] = 2
                            adjacency_matrix[order(x1, y2), order(x1, y1)] = 2

        if event.type == pygame.QUIT:
            finished = True
            print(adjacency_matrix)

        pygame.display.update()

pygame.quit()
