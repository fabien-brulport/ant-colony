import numpy as np


class Node:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index


def euclidean_distance(node1, node2):
    return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5


class Edge:
    def __init__(self, node1, node2, distance_function=euclidean_distance):
        self.node1 = node1
        self.node2 = node2
        self.distance = distance_function(node1, node2)
        self.pheromone = 1

    def value(self, alpha, beta, d_mean):
        return self.pheromone ** alpha * (d_mean / self.distance) ** beta


class Graph:
    def __init__(self, nodes, distance_function=euclidean_distance):
        self.nodes = {node.index: node for node in nodes}
        self._nodes_to_edge = {}

        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                self._nodes_to_edge[(i, j)] = Edge(self.nodes[i], self.nodes[j], distance_function)

    def nodes_to_edge(self, node1, node2):
        return self._nodes_to_edge[min(node1, node2), max(node1, node2)]

    def select_node(self, start, nodes, alpha, beta, d_mean):
        if len(nodes) == 1:
            return nodes[0]
        else:
            mapping = dict(zip(range(len(nodes)), nodes))
            probabilities = np.zeros(len(nodes))
            for i, number in enumerate(nodes):
                probabilities[i] = self.nodes_to_edge(start, number).value(alpha, beta, d_mean)
            probabilities = probabilities / np.sum(probabilities)
            number = mapping[np.random.choice(len(probabilities), p=probabilities)]
            return number

    def global_update_pheromone(self, rho):
        for edge in self._nodes_to_edge.values():
            edge.pheromone = (1 - rho) * edge.pheromone

    def retrieve_pheromone(self):
        pheromones = dict()
        for k, edge in self._nodes_to_edge.items():
            pheromones[k] = edge.pheromone

        return pheromones
