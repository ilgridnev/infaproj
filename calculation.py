import networkx as nx
import numpy as np


adjacency_matrix = [[0, 2, 0, 1, 0, 0, 0, 0, 0],
                    [2, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0, 2, 0, 0],
                    [0, 1, 0, 0, 0, 2, 0, 2, 0],
                    [0, 0, 0, 0, 2, 0, 0, 0, 2],
                    [0, 0, 0, 2, 0, 0, 0, 2, 0],
                    [0, 0, 0, 0, 2, 0, 2, 0, 1],
                    [0, 0, 0, 0, 0, 2, 0, 1, 0]]

"""
adjacency_matrix = [[0, 2, 0, 2],
                    [2, 0, 1, 0],
                    [0, 1, 0, 2],
                    [2, 0, 2, 0]]
"""


def replace(arr, a, b):
    for i in range(len(arr)):
        if arr[i][0] == a:
            arr[i][0] = b
        elif arr[i][1] == a:
            arr[i][1] = b

edges_0 = []
equal = []
edges = []
for i in range(len(adjacency_matrix)):
    for j in range(len(adjacency_matrix)):
        if adjacency_matrix[i][j] != 0:
            if i + 1 < j + 1:
                edges_0.append([i + 1, j + 1])
                if adjacency_matrix[i][j] == 1:
                    equal.append([i + 1, j + 1])

for i in range(len(equal)):
    for j in range(len(edges_0)):
        replace(edges_0, max(equal[i][0], equal[i][1]), min(equal[i][0], equal[i][1]))

for i in range(len(edges_0)):
    if edges_0[i][0] != edges_0[i][1]:
        edges.append(edges_0[i])

G = nx.Graph()
G.add_edges_from(edges)

nodes = list(G.nodes)
q = len(nodes)
p = len(edges)

A = np.zeros(shape=(q-1, p))
for i in range(q - 1):
    for j in range(p):
        if edges[j][0] == nodes[i]:
            A[i][j] = 1
        elif edges[j][1] == nodes[i]:
            A[i][j] = -1
A_T = A.transpose()
Y = np.zeros(shape=(p, p))

for i in range(p):
    for j in range(p):
        if i == j:
            Y[i][j] = 0.5

E = np.array([[0], [1], [0], [0], [0], [0]])

Left_side = A.dot(Y)
Left_side = Left_side.dot(A_T)

Right_side = -A.dot(Y)
Right_side = Right_side.dot(E)

U_0 = np.linalg.solve(Left_side, Right_side)
print(U_0)
print(edges)

