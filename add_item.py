from utils import order
import math


def add_item(draw_func, item_id, p0, screen, adjacency_matrix):
    """Добавить элемент на поле
    :param draw_func Функция отрисовки этого объекта
    :param item_id id элемента который надо добавить
    :param p0 : tuple - пололжение мыши в относительных координатах в момент нажатия
    """
    x, y = p0
    x1 = math.floor(x)
    y1 = math.floor(y)
    x2 = math.ceil(x)
    y2 = math.ceil(y)
    realX = min(x - x1, x2 - x)
    realY = min(y - y1, y2 - y)
    if realX >= realY:
        if abs(y - y1) >= abs(y2 - y):
            if adjacency_matrix[order(x1, y2), order(x2, y2)] == 0 and \
                    adjacency_matrix[order(x2, y2), order(x1, y2)] == 0:
                draw_func(screen, x1, y2, x2, y2)
                adjacency_matrix[order(x1, y2), order(x2, y2)] = item_id
                adjacency_matrix[order(x2, y2), order(x1, y2)] = item_id

        elif adjacency_matrix[order(x1, y1), order(x2, y1)] == 0 and adjacency_matrix[
            order(x2, y1), order(x1, y1)] == 0:
            draw_func(screen, x1, y1, x2, y1)
            adjacency_matrix[order(x1, y1), order(x2, y1)] = item_id
            adjacency_matrix[order(x2, y1), order(x1, y1)] = item_id

    else:
        if abs(x - x1) >= abs(x2 - x):
            if adjacency_matrix[order(x2, y1), order(x2, y2)] == 0 and \
                    adjacency_matrix[order(x2, y2), order(x2, y1)] == 0:
                draw_func(screen, x2, y1, x2, y2)
                adjacency_matrix[order(x2, y1), order(x2, y2)] = item_id
                adjacency_matrix[order(x2, y2), order(x2, y1)] = item_id

        elif adjacency_matrix[order(x1, y1), order(x1, y2)] == 0 and adjacency_matrix[
            order(x1, y2), order(x1, y1)] == 0:
            draw_func(screen, x1, y1, x1, y2)
            adjacency_matrix[order(x1, y1), order(x1, y2)] = item_id
            adjacency_matrix[order(x1, y2), order(x1, y1)] = item_id
