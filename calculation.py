import networkx as nx


class Contours:
    def __init__(self, adjacency_matrix):
        """

        Этот класс выделяет в цепи контуры, на вход принимается матрица смежности,
         которая полность описывает электрическую цепь
        """
        self.adjacency_matrix = adjacency_matrix

        # создаем объект граф
        self.graph = nx.Graph()

        # ассоциируем вершины графа с матрицей смежности
        self.graph.add_edges_from([(i + 1, j + 1) for i in range(len(adjacency_matrix))
                                   for j in range(len(adjacency_matrix)) if adjacency_matrix[i][j] != 0])

        # находим все базисные циклы в графе
        self.cycles = list(nx.cycle_basis(self.graph))

        # добавляем в конец цикла его начальную вершину для удобства расчета
        for i in range(len(self.cycles)):
            self.cycles[i].append(self.cycles[i][0])

        # создаем и заполняем список списков с парами вершин и элементом между ними
        self.element_pairs = []
        for i in range(len(self.cycles)):
            sub = []
            for j in range(len(self.cycles[i])):
                if j + 1 < len(self.cycles[i]):
                    sub.append(
                        (self.cycles[i][j], self.cycles[i][j + 1],
                         self.adjacency_matrix[self.cycles[i][j] - 1][self.cycles[i][j + 1] - 1]))
            self.element_pairs.append(sub)

    def get_contour(self, number):
        """

        принимает итерируемый параметр number, который отвечает за номер контура
        возвращает контур с таким номером
        """
        return self.element_pairs[number]


# создаем матрицу смежности
adjacency_matrix1 = [[0, 1, 0, 1, 0, 0, 0, 0, 0],
                     [1, 0, 0, 0, 2, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 0, 0, 0, 3, 0, 0, 0, 0],
                     [0, 2, 0, 3, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]

contour = Contours(adjacency_matrix1)
print(contour.get_contour(0))
