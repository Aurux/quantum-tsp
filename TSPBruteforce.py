import numpy as np
from itertools import permutations
import matplotlib.pyplot as plt
import time




def create_nodes(n):

    node_array = []
    for i in range(n):
        node = np.round(np.random.rand(2) * 40)
        node_array.append(node)

    return np.array(node_array)


def create_distance_matrix(node_array):

    totalNodes = len(node_array)

    distance_matrix = np.zeros((totalNodes, totalNodes))

    for i in range(totalNodes):
        for j in range(i, totalNodes):
            distance = np.sqrt(
                (node_array[i][0] - node_array[j][0])**2 + (node_array[i][1] - node_array[j][1])**2)
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance

    #print(distance_matrix)
    return distance_matrix


def brute_force(node_array, distance_matrix):
    start = time.time()
    # Basic bruteforce algorithm. Time complexity is O(n!).
    perms = [list(i) for i in permutations(range(1, len(node_array)))]  # Exclude node 0
    bestLength = np.Infinity

    for perm in perms:
        perm = [0] + perm  # Add node 0 at the start
        permLen = calculateLength(distance_matrix, perm)
        if permLen < bestLength:
            bestLength = permLen
            bestPerm = perm

    print("Best permutation = ", bestPerm,"or", bestPerm[::-1])
    end = time.time()

    print("Bruteforce Algorithm took", (end-start), "seconds!")
    return bestPerm, bestLength


def calculateLength(distance_matrix, permutation):
    sum = 0

    for i in range(len(permutation)):
        x = i % len(permutation)
        y = (i+1) % len(permutation)

        sum += distance_matrix[permutation[x], permutation[y]]

    return sum


def draw_graph(node_array, permutation, length, endFlag, fig, ax):
    ax.clear()
    ax.grid()

    ax.scatter(*zip(*node_array), color='blue', zorder=2)
    path = [node_array[i] for i in permutation] + [node_array[permutation[0]]]
    line, = ax.plot(*zip(*path), color='red', zorder=1)

    for i, point in enumerate(node_array):
        ax.text(point[0] * (1 + 0.03), point[1] * (1 + 0.03), i)

    ax.set_title(str("Distance ≈ " + str(round(length, 2))))
    fig.canvas.draw_idle()

    







