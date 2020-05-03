import numpy as np


class Node:
    INDEX = -1

    def __new__(cls, *args, **kwargs):
        """Automatically increments the index number at each instance created."""
        cls.INDEX += 1
        return super().__new__(cls)

    def __init__(self, x, y, name=None):
        self.x = x
        self.y = y
        self.name = name
        self.index = Node.INDEX

    def __eq__(self, other):
        return self.index == other.index


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
    def __init__(self, nodes, distance_function=euclidean_distance, seed=None):
        self.nodes = {node.index: node for node in nodes}
        self.edges = {}
        self.rng = np.random.default_rng(seed=seed)

        # Sorted list of the nodes index
        nodes_index = sorted(self.nodes)

        for i, index_node_1 in enumerate(nodes_index):
            for index_node_2 in nodes_index[i + 1:]:
                self.edges[(index_node_1, index_node_2)] = Edge(self.nodes[index_node_1], self.nodes[index_node_2], distance_function)

    def nodes_to_edge(self, node1, node2):
        return self.edges[min(node1.index, node2.index), max(node1.index, node2.index)]

    def select_node(self, current_node, nodes, alpha, beta, d_mean):
        if len(nodes) == 1:
            return nodes[0]

        probabilities = np.array([self.nodes_to_edge(current_node, node).value(alpha, beta, d_mean) for node in nodes])
        probabilities = probabilities / np.sum(probabilities)
        chosen_node = self.rng.choice(nodes, p=probabilities)
        return chosen_node

    def global_update_pheromone(self, rho):
        for edge in self.edges.values():
            edge.pheromone = (1 - rho) * edge.pheromone

    def retrieve_pheromone(self):
        pheromones = dict()
        for k, edge in self.edges.items():
            pheromones[k] = edge.pheromone

        return pheromones
