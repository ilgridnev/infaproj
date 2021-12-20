# инициализация экрана, настройка частоты обновления, подключение библиотек
import numpy
import pygame.font
from pygame import K_1
from pygame import K_2
from pygame import K_3
from pygame import K_4
from pygame import K_0
from pygame import K_SPACE
from logging import getLogger

import calculation
from drawing import draw_resist, draw_blackbox, draw_battery, draw_description, draw_voltmeter, update_nodes, \
    draw_conductor
from utils import order, is_mouse_in_grid
from add_item import add_item

log = getLogger("main")

pygame.init()
pygame.font.init()
# использумые шрифты
my_font = pygame.font.SysFont('calibri', 30)
second_font = pygame.font.SysFont('calibri', 40)

FPS = 25
screen = pygame.display.set_mode((1000, 600))

# объявление и задание начальных условий для переменных состояний, напряжение нулевое, выводы вольтметра не подключены
volts = 0
exitA = -1
exitB = -1
# Отрисовка узлов схемы, экрана вольтметра, таблицы подсказок
update_nodes(screen)
draw_voltmeter(screen)
draw_description(screen)
# Создание матрицы смежностей и заполнение начальными значениями
adjacency_matrix = numpy.zeros((25, 25))

clock = pygame.time.Clock()
clock.tick(FPS)
finished = False

#  Основной цикл
while not finished:
    # Обновление значения показаний вольтметра
    draw_voltmeter(screen, volts)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # После нажатия на кнопку мыши происходит подключение вольтметра к схеме и выделение подключеннх узлов
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
                # Запускается расчет схемы
                # Обновляется значение напряжения на то, что между узлами, к которым подключен вольтметр
                grid = calculation.Grid(adjacency_matrix)
                # Grid - наследник nx.Graph с функцией расчета схем
                volts = round(grid.get_voltage(exitA, exitB), 2)
            if pygame.key.get_pressed()[K_0]:
                # Сброс значений переменных состояний схемы и обновление правого экрана
                update_nodes(screen)
                volts = 0
                exitA = -1
                exitB = -1
                for i in range(25):
                    for j in range(25):
                        adjacency_matrix[i, j] = 0

            if is_mouse_in_grid(pygame.mouse.get_pos()):
                # Если курсор наведен на схему и нажата клавиша из списка команд, отрисовывается соответств. элемент
                # Первичный вид координат нажатия (не целый)
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
