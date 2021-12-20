# инициализация экрана, настройка частоты обновления, подключение библиотек
import pygame
import numpy
import math
import pygame.font
from pygame import K_1
from pygame import K_2
from pygame import K_3
from pygame import K_4

from pygame import K_0
from pygame import K_SPACE
import calculation

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('calibri', 30)
secondfont = pygame.font.SysFont('calibri', 40)

FPS = 25
screen = pygame.display.set_mode((1000, 600))


def description():
    surf = myfont.render("Описание:", True, (255, 111, 255))
    screen.blit(surf, (50, 270))
    surf = myfont.render("Кнопка 1 / перемычки / ", True, (255, 255, 255))
    screen.blit(surf, (50, 300))
    surf = myfont.render("Кнопка 2 / резисторы / ", True, (0, 255, 255))
    screen.blit(surf, (50, 330))
    surf = myfont.render("Кнопка 3 / источники / ", True, (255, 242, 0))
    screen.blit(surf, (50, 360))
    surf = myfont.render("Кнопка 4 / черный ящик / ???", True, (148, 0, 211))
    screen.blit(surf, (50, 390))
    surf = myfont.render("Кнопка 0 / сброс схемы / =(", True, (124, 255, 0))
    screen.blit(surf, (50, 420))
    surf = myfont.render("Пробел   / обсчет схемы / =)", True, (255, 111, 255))
    screen.blit(surf, (50, 450))


def graphics():
    pygame.draw.rect(screen, (0, 0, 0), (200, 130, 200, 110), 0)
    pygame.draw.rect(screen, (255, 0, 0), (200, 130, 200, 110), 5)
    surf = myfont.render("Voltage A-B", True, (255, 0, 0))

    screen.blit(surf, (230, 200))
    surf = secondfont.render(str(volts) + " [V]", True, (255, 0, 0))
    screen.blit(surf, (250, 160))


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

    pygame.draw.rect(screen, (0, 0, 0), (560, 0, 500, 600), 0)
    surf = secondfont.render("Нормально делай - нормально будет. (с) Карл Гаусс", True, (255, 255, 255))
    screen.blit(surf, (65, 20))
    for i in range(5):
        for j in range(5):
            pygame.draw.circle(screen, (255, 255, 255), (600 + i * 90, 90 * j + 120), 5, 0)


def draw_voltmeter(x1, y1, x2, y2):
    X = 600 + x1 * 90
    Y = 120 + y1 * 90
    XX = 600 + x2 * 90
    YY = 120 + y2 * 90
    XA = (XX + 3 * X) / 4
    YA = (YY + 3 * Y) / 4
    XB = (3 * XX + X) / 4
    YB = (3 * YY + Y) / 4
    R = (abs(XX - X) + abs(YY - Y)) / 4

    pygame.draw.line(screen, (255, 0, 0), (X, Y), (XA, YA), 5)
    pygame.draw.line(screen, (255, 0, 0), (XB, YB), (XX, YY), 5)
    pygame.draw.circle(screen, (255, 0, 0), ((X + XX) / 2, (Y + YY) / 2), R, 5)
    surf = myfont.render("V", True, (255, 0, 0))
    if YY == Y:
        screen.blit(surf, (XA + 14, YA - 14))
    else:
        screen.blit(surf, (XA - 9, YA + 11))


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


def draw_blackbox(x1, y1, x2, y2):
    X = 600 + x1 * 90
    Y = 120 + y1 * 90
    XX = 600 + x2 * 90
    YY = 120 + y2 * 90
    XA = (XX + 2 * X) / 3
    YA = (YY + 2 * Y) / 3
    XB = (2 * XX + X) / 3
    YB = (2 * YY + Y) / 3
    if Y == YY:
        WY1 = YA - abs(XX - X) / 6
        WX1 = XA
        WY2 = YA + abs(XX - X) / 6
        WX2 = XA
        ZY1 = YB - abs(XX - X) / 6
        ZX1 = XB
        ZY2 = YB + abs(XX - X) / 6
        ZX2 = XB
    else:
        WY1 = YA
        WX1 = XA - abs(YY - Y) / 6
        WY2 = YA
        WX2 = XA + abs(YY - Y) / 6
        ZY1 = YB
        ZX1 = XB - abs(YY - Y) / 6
        ZY2 = YB
        ZX2 = XB + abs(YY - Y) / 6

    pygame.draw.line(screen, (148, 0, 211), (X, Y), (XA, YA), 5)
    pygame.draw.line(screen, (148, 0, 211), (XB, YB), (XX, YY), 5)
    pygame.draw.line(screen, (148, 0, 211), (WX1, WY1), (WX2, WY2), 5)
    pygame.draw.line(screen, (148, 0, 211), (WX1, WY1), (ZX1, ZY1), 5)
    pygame.draw.line(screen, (148, 0, 211), (ZX1, ZY1), (ZX2, ZY2), 5)
    pygame.draw.line(screen, (148, 0, 211), (WX2, WY2), (ZX2, ZY2), 5)


def draw_battery(x1, y1, x2, y2):
    X = 600 + x1 * 90
    Y = 120 + y1 * 90
    XX = 600 + x2 * 90
    YY = 120 + y2 * 90
    XA = (4 * XX + 5 * X) / 9
    YA = (4 * YY + 5 * Y) / 9
    XB = (5 * XX + 4 * X) / 9
    YB = (5 * YY + 4 * Y) / 9
    if Y == YY:
        WY1 = YA - abs(XX - X) / 9
        WX1 = XA
        WY2 = YA + abs(XX - X) / 9
        WX2 = XA
        ZY1 = YB - abs(XX - X) / 4
        ZX1 = XB
        ZY2 = YB + abs(XX - X) / 4
        ZX2 = XB
    else:
        WY1 = YA
        WX1 = XA - abs(YY - Y) / 9
        WY2 = YA
        WX2 = XA + abs(YY - Y) / 9
        ZY1 = YB
        ZX1 = XB - abs(YY - Y) / 4
        ZY2 = YB
        ZX2 = XB + abs(YY - Y) / 4

    pygame.draw.line(screen, (255, 242, 0), (X, Y), (XA, YA), 5)
    pygame.draw.line(screen, (255, 242, 0), (XB, YB), (XX, YY), 5)
    pygame.draw.line(screen, (255, 242, 0), (WX1, WY1), (WX2, WY2), 5)

    pygame.draw.line(screen, (255, 242, 0), (ZX1, ZY1), (ZX2, ZY2), 5)


volts = 0
exitA = -1
exitB = -1
knots()
graphics()
description()
adjacency_matrix = numpy.zeros((25, 25))


clock = pygame.time.Clock()
clock.tick(FPS)
finished = False

while not finished:
    calc = calculation.Calculation()
    graphics()
    # volts = calc.calculate(adjacency_matrix)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = (pygame.mouse.get_pos()[0] - 600) / 90
            y = (pygame.mouse.get_pos()[1] - 120) / 90
            x1 = round(x)
            y1 = round(y)

            if exitA == -1:

                exitA = order(x1, y1)+1
                print(exitA)
                pygame.draw.circle(screen, (255, 0, 0), (600 + x1 * 90, 90 * y1 + 120), 7, 0)
                surf = myfont.render("A", True, (255, 0, 0))

                screen.blit(surf, (600 + x1 * 90 -20, 90 * y1 + 120 + 3))

            elif exitB == -1:

                exitB = order(x1, y1)+1
                print(exitB)
                pygame.draw.circle(screen, (255, 0, 0), (600 + x1 * 90, 90 * y1 + 120), 7, 0)
                surf = myfont.render("B", True, (255, 0, 0))

                screen.blit(surf, (600 + x1 * 90 - 20, 90 * y1 + 120 +3))

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[K_SPACE]:
                calc.calculate(adjacency_matrix)
                volts = round(calc.get_voltage(exitA, exitB), 2)
            if pygame.key.get_pressed()[K_0]:
                knots()
                volts = 0
                exitA = -1
                exitB = -1
                for i in range(25):
                    for j in range(25):
                        adjacency_matrix[i, j] = 0

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
                            if adjacency_matrix[order(x1, y2), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x1, y2)] == 0:
                                pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y2 * 90),
                                                 (600 + x2 * 90, 120 + y2 * 90), 5)

                                adjacency_matrix[order(x1, y2), order(x2, y2)] = 1
                                adjacency_matrix[order(x2, y2), order(x1, y2)] = 1


                        elif adjacency_matrix[order(x1, y1), order(x2, y1)] == 0 and adjacency_matrix[
                            order(x2, y1), order(x1, y1)] == 0:
                            pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y1 * 90),
                                             (600 + x2 * 90, 120 + y1 * 90), 5)
                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 1
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 1

                    else:
                        if abs(x - x1) >= abs(x2 - x):
                            if adjacency_matrix[order(x2, y1), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x2, y1)] == 0:
                                pygame.draw.line(screen, (255, 255, 255), (600 + x2 * 90, 120 + y1 * 90),
                                                 (600 + x2 * 90, 120 + y2 * 90), 5)
                                adjacency_matrix[order(x2, y1), order(x2, y2)] = 1
                                adjacency_matrix[order(x2, y2), order(x2, y1)] = 1

                        elif adjacency_matrix[order(x1, y1), order(x1, y2)] == 0 and adjacency_matrix[
                            order(x1, y2), order(x1, y1)] == 0:
                            pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y1 * 90),
                                             (600 + x1 * 90, 120 + y2 * 90), 5)
                            adjacency_matrix[order(x1, y1), order(x1, y2)] = 1
                            adjacency_matrix[order(x1, y2), order(x1, y1)] = 1

                if pygame.key.get_pressed()[K_2]:
                    realX = min(x - x1, x2 - x)
                    realY = min(y - y1, y2 - y)

                    if realX >= realY:
                        if abs(y - y1) >= abs(y2 - y):
                            if adjacency_matrix[order(x1, y2), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x1, y2)] == 0:
                                draw_resist(x1, y2, x2, y2)

                                adjacency_matrix[order(x1, y2), order(x2, y2)] = 2
                                adjacency_matrix[order(x2, y2), order(x1, y2)] = 2


                        elif adjacency_matrix[order(x1, y1), order(x2, y1)] == 0 and adjacency_matrix[
                            order(x2, y1), order(x1, y1)] == 0:
                            draw_resist(x1, y1, x2, y1)

                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 2
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 2

                    else:
                        if abs(x - x1) >= abs(x2 - x):
                            if adjacency_matrix[order(x2, y1), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x2, y1)] == 0:
                                draw_resist(x2, y1, x2, y2)

                                adjacency_matrix[order(x2, y1), order(x2, y2)] = 2
                                adjacency_matrix[order(x2, y2), order(x2, y1)] = 2

                        elif adjacency_matrix[order(x1, y1), order(x1, y2)] == 0 and adjacency_matrix[
                            order(x1, y2), order(x1, y1)] == 0:
                            draw_resist(x1, y1, x1, y2)

                            adjacency_matrix[order(x1, y1), order(x1, y2)] = 2
                            adjacency_matrix[order(x1, y2), order(x1, y1)] = 2
                if pygame.key.get_pressed()[K_3]:
                    realX = min(x - x1, x2 - x)
                    realY = min(y - y1, y2 - y)

                    if realX >= realY:
                        if abs(y - y1) >= abs(y2 - y):
                            if adjacency_matrix[order(x1, y2), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x1, y2)] == 0:
                                draw_battery(x1, y2, x2, y2)

                                adjacency_matrix[order(x1, y2), order(x2, y2)] = 3
                                adjacency_matrix[order(x2, y2), order(x1, y2)] = 3


                        elif adjacency_matrix[order(x1, y1), order(x2, y1)] == 0 and adjacency_matrix[
                            order(x2, y1), order(x1, y1)] == 0:
                            draw_battery(x1, y1, x2, y1)

                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 3
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 3

                    else:
                        if abs(x - x1) >= abs(x2 - x):
                            if adjacency_matrix[order(x2, y1), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x2, y1)] == 0:
                                draw_battery(x2, y1, x2, y2)

                                adjacency_matrix[order(x2, y1), order(x2, y2)] = 3
                                adjacency_matrix[order(x2, y2), order(x2, y1)] = 3

                        elif adjacency_matrix[order(x1, y1), order(x1, y2)] == 0 and adjacency_matrix[
                            order(x1, y2), order(x1, y1)] == 0:
                            draw_battery(x1, y1, x1, y2)

                            adjacency_matrix[order(x1, y1), order(x1, y2)] = 3
                            adjacency_matrix[order(x1, y2), order(x1, y1)] = 3
                if pygame.key.get_pressed()[K_4]:
                    realX = min(x - x1, x2 - x)
                    realY = min(y - y1, y2 - y)

                    if realX >= realY:
                        if abs(y - y1) >= abs(y2 - y):
                            if adjacency_matrix[order(x1, y2), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x1, y2)] == 0:
                                draw_blackbox(x1, y2, x2, y2)

                                adjacency_matrix[order(x1, y2), order(x2, y2)] = 5
                                adjacency_matrix[order(x2, y2), order(x1, y2)] = 5


                        elif adjacency_matrix[order(x1, y1), order(x2, y1)] == 0 and adjacency_matrix[
                            order(x2, y1), order(x1, y1)] == 0:
                            draw_blackbox(x1, y1, x2, y1)

                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 5
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 5

                    else:
                        if abs(x - x1) >= abs(x2 - x):
                            if adjacency_matrix[order(x2, y1), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x2, y1)] == 0:
                                draw_blackbox(x2, y1, x2, y2)

                                adjacency_matrix[order(x2, y1), order(x2, y2)] = 5
                                adjacency_matrix[order(x2, y2), order(x2, y1)] = 5

                        elif adjacency_matrix[order(x1, y1), order(x1, y2)] == 0 and adjacency_matrix[
                            order(x1, y2), order(x1, y1)] == 0:
                            draw_blackbox(x1, y1, x1, y2)

                            adjacency_matrix[order(x1, y1), order(x1, y2)] = 5
                            adjacency_matrix[order(x1, y2), order(x1, y1)] = 5
        if event.type == pygame.QUIT:
            finished = True
            print(adjacency_matrix)

        pygame.display.update()

pygame.quit()
# HI. IT'S ME