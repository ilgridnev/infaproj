import networkx as nx
import numpy as np


class Calculation:
    """
    Данный класс производит просчет электрической цепи методом узловых потенциалов:
    Каждой вершине планарного графа цепи сопостовляется свой потенциал. Затем составляется и решается СЛУ
    """
    def __init__(self):
        """
        Инициализация необходимых для описания поля потенциалов списков
        """
        self.U_0 = []
        self.equal = []
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

        def replace(arr, a, b):
            """
            вспомогательная функция меняющая все элементы a на b в списке arr
            """
            for i in range(len(arr)):
                if arr[i][0] == a:
                    arr[i][0] = b
                elif arr[i][1] == a:
                    arr[i][1] = b

        edges_0 = []
        self.equal = []
        self.edges = []
        for i in range(len(adjacency_matrix)):
            for j in range(len(adjacency_matrix)):
                if adjacency_matrix[i][j] != 0:
                    if i + 1 < j + 1:
                        edges_0.append([i + 1, j + 1])
                        if adjacency_matrix[i][j] == 1:
                            self.equal.append([i + 1, j + 1])

        for i in range(len(self.equal)):
            for j in range(len(edges_0)):
                replace(edges_0, max(self.equal[i][0], self.equal[i][1]), min(self.equal[i][0], self.equal[i][1]))

        for i in range(len(edges_0)):
            if edges_0[i][0] != edges_0[i][1]:
                self.edges.append(edges_0[i])
        G = nx.Graph()
        G.add_edges_from(self.edges)

        self.nodes = list(G.nodes)
        q = len(self.nodes)
        p = len(self.edges)

        A = np.zeros(shape=(q - 1, p))
        for i in range(q - 1):
            for j in range(p):
                if self.edges[j][0] == self.nodes[i]:
                    A[i][j] = 1
                elif self.edges[j][1] == self.nodes[i]:
                    A[i][j] = -1
        A_T = A.transpose()
        Y = np.zeros(shape=(p, p))

        for i in range(p):
            for j in range(p):
                if i == j:
                    Y[i][j] = 0.5

        E = np.zeros(shape=(p, 1))
        for i in range(p):
            if adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 3:
                E[i][0] = 1

        Left_side = A.dot(Y)
        Left_side = Left_side.dot(A_T)

        Right_side = -A.dot(Y)
        Right_side = Right_side.dot(E)

        self.U_0 = np.linalg.solve(Left_side, Right_side)
        self.U_0 = np.append(self.U_0, [0])

    def get_voltage(self, node1, node2):
        """
        node1 - номер узла 1 в матрице смежности
        node2 - номер узла 2 в матрице смежности

        возвращает напряжение (абсолютную разность потенциалов)
        """
        for i in range(len(self.equal)):
            if node1 in self.equal[i]:
                node1 = min(self.equal[i][0], self.equal[i][1])
            if node2 in self.equal[i]:
                node2 = min(self.equal[i][0], self.equal[i][1])
        return abs(self.U_0[self.nodes.index(node1)] - self.U_0[self.nodes.index(node2)])

calc = Calculation()
calc.calculate([[0, 2, 0, 3, 0, 0, 0, 0, 0],
                [2, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [3, 0, 0, 0, 0, 0, 2, 0, 0],
                [0, 1, 0, 0, 0, 2, 0, 2, 0],
                [0, 0, 0, 0, 2, 0, 0, 0, 2],
                [0, 0, 0, 2, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 2, 0, 2, 0, 1],
                [0, 0, 0, 0, 0, 2, 0, 1, 0]])
print(calc.get_voltage(1, 5))
calc.calculate([[0, 2, 0, 3],
                [2, 0, 1, 0],
                [0, 1, 0, 2],
                [3, 0, 2, 0]])
print(calc.get_voltage(1, 3))
