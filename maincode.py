# инициализация экрана, настройка частоты обновления, подключение библиотек
import numpy
import math
import pygame.font
from pygame import K_1
from pygame import K_2
from pygame import K_3
from pygame import K_4

import logging
from logging import basicConfig
from logging import getLogger

from pygame import K_0
from pygame import K_SPACE
import calculation
from drawing import draw_resist, draw_blackbox, draw_battery, draw_description, draw_voltmeter, update_nodes
from utils import order

log = getLogger("main")

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('calibri', 30)
second_font = pygame.font.SysFont('calibri', 40)

FPS = 25
screen = pygame.display.set_mode((1000, 600))

volts = 0
exitA = -1
exitB = -1
update_nodes(screen)
draw_voltmeter(screen)
draw_description(screen)
adjacency_matrix = numpy.zeros((25, 25))

clock = pygame.time.Clock()
clock.tick(FPS)
finished = False

while not finished:
    draw_voltmeter(screen, volts)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Определяем координаты ближайшего узла сетки
            x1 = round((pygame.mouse.get_pos()[0] - 600) / 90)
            y1 = round((pygame.mouse.get_pos()[1] - 120) / 90)
            if exitA == -1:
                exitA = order(x1, y1) + 1
                log.debug(exitA)
                pygame.draw.circle(screen, (255, 0, 0), (600 + x1 * 90, 90 * y1 + 120), 7, 0)
                surf = my_font.render("A", True, (255, 0, 0))
                screen.blit(surf, (600 + x1 * 90 - 20, 90 * y1 + 120 + 3))
            elif exitB == -1:
                exitB = order(x1, y1) + 1
                log.debug(exitB)
                pygame.draw.circle(screen, (255, 0, 0), (600 + x1 * 90, 90 * y1 + 120), 7, 0)
                surf = my_font.render("B", True, (255, 0, 0))
                screen.blit(surf, (600 + x1 * 90 - 20, 90 * y1 + 120 + 3))

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[K_SPACE]:
                grid = calculation.Grid(adjacency_matrix)
                # Grid - наследник nx.Graph с функцией расчета схем
                volts = round(grid.get_voltage(exitA, exitB), 2)
            if pygame.key.get_pressed()[K_0]:
                # Reset
                update_nodes(screen)
                volts = 0
                exitA = -1
                exitB = -1
                for i in range(25):
                    for j in range(25):
                        adjacency_matrix[i, j] = 0

            if (pygame.mouse.get_pos()[0] >= 600) and (pygame.mouse.get_pos()[0] <= 960) and (
                    pygame.mouse.get_pos()[1] >= 120) and (pygame.mouse.get_pos()[1] <= 480):  # TODO mouse in grid
                x = (pygame.mouse.get_pos()[0] - 600) / 90
                y = (pygame.mouse.get_pos()[1] - 120) / 90
                x1 = math.floor(x)
                y1 = math.floor(y)
                x2 = math.ceil(x)
                y2 = math.ceil(y)
                realX = min(x - x1, x2 - x)
                realY = min(y - y1, y2 - y)
                if pygame.key.get_pressed()[K_1]:
                    if realX >= realY: # Вертикальное
                        if abs(y - y1) >= abs(y2 - y):
                            if adjacency_matrix[order(x1, y2), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x1, y2)] == 0:
                                # Проверка что это поле пустое

                                # TODO нарисовать перемучку
                                # TODO Какая то муть с (x1, y1) вынести
                                pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y2 * 90),
                                                 (600 + x2 * 90, 120 + y2 * 90), 5)

                                # TODO Разобраться с мутью с x1 y1 и перенести в блок после проверки на
                                #  вертиклаьсность\горзонтальность
                                adjacency_matrix[order(x1, y2), order(x2, y2)] = 1
                                adjacency_matrix[order(x2, y2), order(x1, y2)] = 1


                        elif adjacency_matrix[order(x1, y1), order(x2, y1)] == 0 and adjacency_matrix[
                            order(x2, y1), order(x1, y1)] == 0:
                            # TODO вынести отрисовку
                            pygame.draw.line(screen, (255, 255, 255), (600 + x1 * 90, 120 + y1 * 90),
                                             (600 + x2 * 90, 120 + y1 * 90), 5)
                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 1
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 1

                    else: # TODO Аналогичное с верхом
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
                    if realX < realY:
                        (x, y) = (y, x)
                        (x1, y1) = (y1, x1)
                        (x2, y2) = (y2, x2)

                        if abs(y - y1) >= abs(y2 - y):
                            if adjacency_matrix[order(x1, y2), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x1, y2)] == 0:
                                draw_resist(screen, x1, y2, x2, y2)

                                adjacency_matrix[order(x1, y2), order(x2, y2)] = 2
                                adjacency_matrix[order(x2, y2), order(x1, y2)] = 2


                        elif adjacency_matrix[order(x1, y1), order(x2, y1)] == 0 and adjacency_matrix[
                            order(x2, y1), order(x1, y1)] == 0:
                            draw_resist(screen, x1, y1, x2, y1)

                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 2
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 2

                    else:
                        if abs(x - x1) >= abs(x2 - x):
                            if adjacency_matrix[order(x2, y1), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x2, y1)] == 0:
                                draw_resist(screen, x2, y1, x2, y2)

                                adjacency_matrix[order(x2, y1), order(x2, y2)] = 2
                                adjacency_matrix[order(x2, y2), order(x2, y1)] = 2

                        elif adjacency_matrix[order(x1, y1), order(x1, y2)] == 0 and adjacency_matrix[
                            order(x1, y2), order(x1, y1)] == 0:
                            draw_resist(screen, x1, y1, x1, y2)

                            adjacency_matrix[order(x1, y1), order(x1, y2)] = 2
                            adjacency_matrix[order(x1, y2), order(x1, y1)] = 2
                if pygame.key.get_pressed()[K_3]:
                    if realX >= realY:
                        if abs(y - y1) >= abs(y2 - y):
                            if adjacency_matrix[order(x1, y2), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x1, y2)] == 0:
                                draw_battery(screen, x1, y2, x2, y2)

                                adjacency_matrix[order(x1, y2), order(x2, y2)] = 3
                                adjacency_matrix[order(x2, y2), order(x1, y2)] = 3


                        elif adjacency_matrix[order(x1, y1), order(x2, y1)] == 0 and adjacency_matrix[
                            order(x2, y1), order(x1, y1)] == 0:
                            draw_battery(screen, x1, y1, x2, y1)

                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 3
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 3

                    else:
                        if abs(x - x1) >= abs(x2 - x):
                            if adjacency_matrix[order(x2, y1), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x2, y1)] == 0:
                                draw_battery(screen, x2, y1, x2, y2)

                                adjacency_matrix[order(x2, y1), order(x2, y2)] = 3
                                adjacency_matrix[order(x2, y2), order(x2, y1)] = 3

                        elif adjacency_matrix[order(x1, y1), order(x1, y2)] == 0 and adjacency_matrix[
                            order(x1, y2), order(x1, y1)] == 0:
                            draw_battery(screen, x1, y1, x1, y2)

                            adjacency_matrix[order(x1, y1), order(x1, y2)] = 3
                            adjacency_matrix[order(x1, y2), order(x1, y1)] = 3
                if pygame.key.get_pressed()[K_4]:

                    if realX >= realY:
                        if abs(y - y1) >= abs(y2 - y):
                            if adjacency_matrix[order(x1, y2), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x1, y2)] == 0:
                                draw_blackbox(screen, x1, y2, x2, y2)

                                adjacency_matrix[order(x1, y2), order(x2, y2)] = 5
                                adjacency_matrix[order(x2, y2), order(x1, y2)] = 5


                        elif adjacency_matrix[order(x1, y1), order(x2, y1)] == 0 and adjacency_matrix[
                            order(x2, y1), order(x1, y1)] == 0:
                            draw_blackbox(screen, x1, y1, x2, y1)

                            adjacency_matrix[order(x1, y1), order(x2, y1)] = 5
                            adjacency_matrix[order(x2, y1), order(x1, y1)] = 5

                    else:
                        if abs(x - x1) >= abs(x2 - x):
                            if adjacency_matrix[order(x2, y1), order(x2, y2)] == 0 and \
                                    adjacency_matrix[order(x2, y2), order(x2, y1)] == 0:
                                draw_blackbox(screen, x2, y1, x2, y2)

                                adjacency_matrix[order(x2, y1), order(x2, y2)] = 5
                                adjacency_matrix[order(x2, y2), order(x2, y1)] = 5

                        elif adjacency_matrix[order(x1, y1), order(x1, y2)] == 0 and adjacency_matrix[
                            order(x1, y2), order(x1, y1)] == 0:
                            draw_blackbox(screen, x1, y1, x1, y2)

                            adjacency_matrix[order(x1, y1), order(x1, y2)] = 5
                            adjacency_matrix[order(x1, y2), order(x1, y1)] = 5
        if event.type == pygame.QUIT:
            finished = True
            print(adjacency_matrix)

        pygame.display.update()

pygame.quit()
