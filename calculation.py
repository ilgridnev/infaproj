import networkx as nx
import numpy as np

from utils import matrix_to_list


class Grid(nx.Graph):
    def __init__(self, adjacency_matrix):
        super().__init__()
        self.matrix = adjacency_matrix
        self.U_0 = []  # Напряжение между узлами
        edges = matrix_to_list(adjacency_matrix)
        self.add_edges_from(edges)
        num_nodes = len(self.nodes)
        num_edges = len(self.edges)

        # заполняем необходимые для вычислений матрицы
        if num_nodes - 1 >= 0:
            connections_matrix = np.zeros(shape=(num_nodes - 1, num_edges))
        else:
            connections_matrix = np.zeros(shape=(num_nodes, num_edges))

        for i in range(num_nodes - 1):
            for j in range(num_edges):
                if self.edges[j][0] == self.nodes[i]:
                    connections_matrix[i][j] = 1
                elif self.edges[j][1] == self.nodes[i]:
                    connections_matrix[i][j] = -1
        connections_transpose = connections_matrix.transpose()
        conductor_matrix = np.zeros(shape=(num_edges, num_edges))

        # Расчет узловых потенциалов
        for i in range(num_edges):
            if adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 1:
                # TODO Что за магические цыфрыэ переделай с использованием функции get_element из utils
                conductor_matrix[i][i] = 1000
                # TODO Все эти магические константы вынести в конфиг и импортировать
            elif adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 2:
                conductor_matrix[i][i] = 0.5
            elif adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 3:
                conductor_matrix[i][i] = 100000
            elif adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 4:
                conductor_matrix[i][i] = 0.2

        eds_matrix = np.zeros(shape=(num_edges, 1))
        for i in range(num_edges):
            if adjacency_matrix[self.edges[i][0] - 1][self.edges[i][1] - 1] == 3:
                eds_matrix[i][0] = 1

        # составляем матричное уравнение
        Left_side = connections_matrix.dot(conductor_matrix)
        Left_side = Left_side.dot(connections_transpose)

        Right_side = -connections_matrix.dot(conductor_matrix)
        Right_side = Right_side.dot(eds_matrix)

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
            res = abs(self.U_0[list(self.nodes).index(node1)] - self.U_0[list(self.nodes).index(node2)])
            # TODO Почему пишем .index а не [ ] ?
            return round(res, 2)
        else:
            return 0.0

