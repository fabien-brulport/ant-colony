import numpy as np


class ACO:
    def __init__(self, graph):
        self.graph = graph
        self.ants = []

    def solve(self, alpha=1, beta=1, rho=0.1, n_ants=20, n_iterations=10, verbose=False, plotter=None):
        d_mean = np.sum(edge.distance for edge in self.graph.edges.values()) / (len(self.graph.edges))
        min_distance = d_mean * len(self.graph.nodes)
        self.ants = []
        best_path = None
        starts = list(range(len(self.graph.nodes)))
        for i in range(n_ants):
            self.ants.append(Ant(self.graph, d_mean))
        for iteration in range(n_iterations):
            if verbose and iteration % 100 == 0:
                print('Iteration {}/{}'.format(iteration, n_iterations))
            np.random.shuffle(starts)
            for i, ant in enumerate(self.ants):
                ant.initialize(starts[i % len(starts)])
                ant.one_iteration(alpha, beta)
            self.graph.global_update_pheromone(rho)

            for ant in self.ants:
                ant.local_update_pheromone(min_distance / len(self.ants))
                if ant.distance < min_distance:
                    min_distance = ant.distance
                    best_path = ant.path

            if plotter is not None:
                plotter.update(best_path, min_distance)

        return best_path, min_distance


class Ant:
    def __init__(self, graph, d_mean=1.):
        self.position = None
        self.nodes_to_visit = []
        self.graph = graph
        self.distance = 0
        self.edges_visited = []
        self.path = []
        self.d_mean = d_mean

    def initialize(self, start):
        self.position = start
        self.nodes_to_visit = [node.index for i, node in self.graph.nodes.items() if i != self.position]
        self.distance = 0
        self.edges_visited = []
        self.path = [start]

    def one_iteration(self, alpha, beta):
        while self.nodes_to_visit:
            node_index = self.graph.select_node(self.position, self.nodes_to_visit, alpha, beta, self.d_mean)
            self.nodes_to_visit.remove(node_index)
            self.path.append(node_index)
            self.edges_visited.append(self.graph.nodes_to_edge(self.position, node_index))
            self.distance += self.graph.nodes_to_edge(self.position, node_index).distance
            self.position = node_index
        self.path.append(self.path[0])
        self.distance += self.graph.nodes_to_edge(self.position, self.path[0]).distance

    def local_update_pheromone(self, d):
        for edge in self.edges_visited:
            edge.pheromone += d / self.distance
