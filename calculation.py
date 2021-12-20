import networkx as nx
import numpy as np

from config import *
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
                if edges[j][0] == list(self.nodes)[i]:
                    connections_matrix[i][j] = 1
                elif edges[j][1] == list(self.nodes)[i]:
                    connections_matrix[i][j] = -1
        connections_transpose = connections_matrix.transpose()
        conductor_matrix = np.zeros(shape=(num_edges, num_edges))

        # Расчет узловых потенциалов
        for i in range(num_edges):
            if adjacency_matrix[edges[i][0] - 1][edges[i][1] - 1] == 1:
                conductor_matrix[i][i] = R_1
            elif adjacency_matrix[edges[i][0] - 1][edges[i][1] - 1] == 2:
                conductor_matrix[i][i] = r_1
            elif adjacency_matrix[edges[i][0] - 1][edges[i][1] - 1] == 3:
                conductor_matrix[i][i] = R_2
            elif adjacency_matrix[edges[i][0] - 1][edges[i][1] - 1] == 4:
                conductor_matrix[i][i] = r_2

        eds_matrix = np.zeros(shape=(num_edges, 1))
        for i in range(num_edges):
            if adjacency_matrix[edges[i][0] - 1][edges[i][1] - 1] == 3:
                eds_matrix[i][0] = 1

        # составляем матричное уравнение
        left_side = connections_matrix.dot(conductor_matrix)
        left_side = left_side.dot(connections_transpose)

        right_side = -connections_matrix.dot(conductor_matrix)
        right_side = right_side.dot(eds_matrix)

        # решаем систему уравнений с помощью метода нахождения обратной матрицы
        self.U_0 = np.linalg.solve(left_side, right_side)
        self.U_0 = np.append(self.U_0, [0])

    def get_voltage(self, node1, node2):
        """
        node1 - номер узла 1 в матрице смежности
        node2 - номер узла 2 в матрице смежности

        возвращает напряжение (абсолютную разность потенциалов)
        """
        if node1 in self.nodes and node2 in self.nodes:
            res = abs(self.U_0[list(self.nodes).index(node1)] - self.U_0[list(self.nodes).index(node2)])
            return res
        else:
            return 0.0

