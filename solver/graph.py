import numpy as np


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._number = None

    @property
    def number(self):
        if self._number is None:
            raise AttributeError("Number attribute has not been set.")
        else:
            return self._number

    @number.setter
    def number(self, number):
        self._number = number


class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.distance = ((self.node1.x - self.node2.x) ** 2 + (self.node1.y - self.node2.y) ** 2) ** 0.5
        self.pheromone = 1

    def value(self, alpha, beta, d_mean):
        return self.pheromone ** alpha * (d_mean / self.distance) ** beta


class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self._nodes_to_edge = {}

        for i in range(len(self.nodes)):
            self.nodes[i].number = i
            for j in range(i + 1, len(self.nodes)):
                self._nodes_to_edge[(i, j)] = Edge(self.nodes[i], self.nodes[j])

    def nodes_to_edge(self, node1, node2):
        return self._nodes_to_edge[min(node1, node2), max(node1, node2)]

    def select_node(self, start, nodes, alpha, beta, d_mean):
        if len(nodes) == 1:
            return nodes[0]
        else:
            mapping = dict(zip(range(len(nodes)), nodes))
            probabilities = np.zeros(len(nodes))
            for i, number in enumerate(nodes):
                probabilities[i] = self.nodes_to_edge(start, number).value(
                    alpha, beta, d_mean)
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
