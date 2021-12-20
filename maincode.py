# инициализация экрана, настройка частоты обновления, подключение библиотек
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
from drawing import draw_resist, draw_blackbox, draw_battery, draw_description, draw_voltmeter, knots
from utils import order

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('calibri', 30)
second_font = pygame.font.SysFont('calibri', 40)

FPS = 25
screen = pygame.display.set_mode((1000, 600))

volts = 0
exitA = -1
exitB = -1
knots()
draw_voltmeter()
draw_description()
adjacency_matrix = numpy.zeros((25, 25))


clock = pygame.time.Clock()
clock.tick(FPS)
finished = False

while not finished:
    calc = calculation.Calculation()
    draw_voltmeter()
    # volts = calc.calculate(adjacency_matrix)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = (pygame.mouse.get_pos()[0] - 600) / 90
            y = (pygame.mouse.get_pos()[1] - 120) / 90
            x1 = round(x)
            y1 = round(y)

            if exitA == -1:

                exitA = order(x1, y1) + 1
                print(exitA)
                pygame.draw.circle(screen, (255, 0, 0), (600 + x1 * 90, 90 * y1 + 120), 7, 0)
                surf = my_font.render("A", True, (255, 0, 0))

                screen.blit(surf, (600 + x1 * 90 - 20, 90 * y1 + 120 + 3))

            elif exitB == -1:

                exitB = order(x1, y1) + 1
                print(exitB)
                pygame.draw.circle(screen, (255, 0, 0), (600 + x1 * 90, 90 * y1 + 120), 7, 0)
                surf = my_font.render("B", True, (255, 0, 0))

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