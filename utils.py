from config import ELEMENTS


def matrix_to_list(matrix) -> list:
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




