import networkx as nx
import numpy as np


class Calculation:
    """
    Данный класс производит просчёт электрической цепи методом узловых потенциалов:
    Каждой вершине планарного графа цепи сопостовляется свой потенциал. Затем составляется и решается СЛУ
    """

    def __init__(self):
        """
        Инициализация необходимых для описания поля потенциалов списков
        """
        self.U_0 = []
        self.edges = []
        self.nodes = []

    def calculate(self, adjacency_matrix):
        """
        adjacency_matrix -- матрица смежности, описывает как соеденины элементы в цепи
        Реализованный алгоритм работает следующим образом: вначале переводим матрицу смежности в список смежности,
        после этого находятся все эквипотенциальные ребра графа - вершины соединенные таким ребром отождествляются.
        После этого заполняются матрицы A, Y, E -- матрицы отвечающие за присодинение элементов к узлам, матрица проводимости
        и матрица источников эдс соответсвенно. Из теории электрических цепей известно, что A*Y*A_T*U_0 = - A*Y*E,
        где U_0 вектор потенциалов в узлах. Решаем полученную систему методом numpy.linalg.
        """

        # пересчитываем матрицу смежности в список смежности
        self.edges = []
        for i in range(len(adjacency_matrix)):
            for j in range(len(adjacency_matrix)):
                if adjacency_matrix[i][j] != 0:
                    if i + 1 < j + 1:
                        self.edges.append([i + 1, j + 1])

        # создаем объект класса Graph, который облегчает работу с планарным графом цепи
        G = nx.Graph()
        G.add_edges_from(self.edges)

        self.nodes = list(G.nodes)
        q = len(self.nodes)
        p = len(self.edges)

        # заполняем необходимые для вычислений матрицы
        if q - 1 >= 0:
            A = np.zeros(shape=(q - 1, p))
        else:
            A = np.zeros(shape=(q, p))

        for i in range(q - 1):
            for j in range(p):
                if self.edges[j][0] == self.nodes[i]:
                    A[i][j] = 1
                elif self.edges[j][1] == self.nodes[i]:
                    A[i][j] = -1
        A_T = A.transpose()
        Y = np.zeros(shape=(p, p))

        # описание внутренней логики цепи
        for i in range(p):
            if adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 1:
                Y[i][i] = 1000
            elif adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 2:
                Y[i][i] = 0.5
            elif adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 3:
                Y[i][i] = 100000
            elif adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 4:
                Y[i][i] = 0.2

        E = np.zeros(shape=(p, 1))
        for i in range(p):
            if adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 3:
                E[i][0] = 1

        # составляем матричное уравнение
        Left_side = A.dot(Y)
        Left_side = Left_side.dot(A_T)

        Right_side = -A.dot(Y)
        Right_side = Right_side.dot(E)

        # решаем систему уравнений с помощью метода нахождения обратной матрицы
        self.U_0 = np.linalg.solve(Left_side, Right_side)
        self.U_0 = np.append(self.U_0, [0])

    def get_voltage(self, node1, node2):
        """
        node1 - номер узла 1 в матрице смежности
        node2 - номер узла 2 в матрице смежности

        возвращает напряжение (абсолютную разность потенциалов)
        """
        if node1 in self.nodes and node2 in self.nodes:
            res = abs(self.U_0[self.nodes.index(node1)] - self.U_0[self.nodes.index(node2)])
            return round(res, 2)
        else:
            return 0.0
