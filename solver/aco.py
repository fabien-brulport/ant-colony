import numpy as np


class ACO:
    def __init__(self, graph, seed=None):
        self.graph = graph
        self.ants = []
        self.rng = np.random.default_rng(seed=seed)

    def solve(self, alpha=1, beta=1, rho=0.1, n_ants=20, n_iterations=10, verbose=False, plotter=None):
        d_mean = np.sum(edge.distance for edge in self.graph.edges.values()) / (len(self.graph.edges))
        min_distance = d_mean * len(self.graph.nodes)
        self.ants = []
        best_path = None
        starts = list(self.graph.nodes.values())
        for i in range(n_ants):
            self.ants.append(Ant(self.graph, d_mean))
        for iteration in range(n_iterations):
            if verbose and iteration % 100 == 0:
                print('Iteration {}/{}'.format(iteration, n_iterations))
            for ant in self.ants:
                ant.initialize(starts[self.rng.integers(len(starts))])
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
        self.nodes_to_visit = [node for node in self.graph.nodes.values() if node != self.position]
        self.distance = 0
        self.edges_visited = []
        self.path = [start]

    def one_iteration(self, alpha, beta):
        while self.nodes_to_visit:
            chosen_node = self.graph.select_node(self.position, self.nodes_to_visit, alpha, beta, self.d_mean)
            self.nodes_to_visit.remove(chosen_node)
            self.path.append(chosen_node)
            chosen_edge = self.graph.nodes_to_edge(self.position, chosen_node)
            self.edges_visited.append(chosen_edge)
            self.distance += chosen_edge.distance
            self.position = chosen_node
        self.path.append(self.path[0])
        self.distance += self.graph.nodes_to_edge(self.position, self.path[0]).distance

    def local_update_pheromone(self, d):
        for edge in self.edges_visited:
            edge.pheromone += d / self.distance
