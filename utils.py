from config import ELEMENTS


def matrix_to_list(matrix) -> list:
    """"Перевод матрицы смежности в список смежности"""
    res = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != 0:
                if i + 1 < j + 1:
                    res.append([i + 1, j + 1])
    return res


def order(x, y):
    """
    функция принимает на вход  х и у номера узла и возвращает номер узла в матрице смежности
    :return:
    """
    return x * 5 + y


def element_type(num: int) -> str:
    """Получить тип элемента по номеру"""
    return ELEMENTS[num]


def is_field_empty(matrix, p1, p2) -> bool:
    """"Занято ли это поле в сетке
    :param p1 : tuple - x1, y1 - координаты точки начала объекта
    :param p2 : tuple - x2, y2 - координаты точки конца объекта
    """
    return True # TODO
