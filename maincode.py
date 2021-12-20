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
from drawing import draw_resist, draw_blackbox, draw_battery, draw_description, draw_voltmeter, update_nodes, \
    draw_conductor
from utils import order, is_mouse_in_grid
from add_item import add_item
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

            if is_mouse_in_grid(pygame.mouse.get_pos()):
                x = (pygame.mouse.get_pos()[0] - 600) / 90
                y = (pygame.mouse.get_pos()[1] - 120) / 90
                mouse_pos = x, y
                if pygame.key.get_pressed()[K_1]:
                    add_item(draw_conductor, 1, mouse_pos, screen, adjacency_matrix)
                if pygame.key.get_pressed()[K_2]:
                    add_item(draw_resist, 2, mouse_pos, screen, adjacency_matrix)
                if pygame.key.get_pressed()[K_3]:
                    add_item(draw_battery, 3, mouse_pos, screen, adjacency_matrix)
                if pygame.key.get_pressed()[K_4]:
                    add_item(draw_blackbox, 4, mouse_pos, screen, adjacency_matrix)
        if event.type == pygame.QUIT:
            finished = True
            print(adjacency_matrix)

        pygame.display.update()

pygame.quit()
