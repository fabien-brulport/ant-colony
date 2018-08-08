from graph import *
import numpy as np


class ACO:
    def __init__(self, nodes):
        self.graph = Graph(nodes)
        self.ants = []
        self.paths = []
        self.pheromones = []
        self.distances = []

    def solve(self, alpha=1, beta=1, rho=0.1, n_ants=20, n_iterations=10, verbose=False):
        d = self.init_solution(alpha, beta)
        min_distance = np.inf
        self.ants = []
        starts = list(range(len(self.graph.nodes)))
        for i in range(n_ants):
            self.ants.append(Ant(self.graph))
        for iteration in range(n_iterations):
            if verbose and iteration % 100 == 0:
                print('Iteration {}/{}'.format(iteration, n_iterations))
            np.random.shuffle(starts)
            for i, ant in enumerate(self.ants):
                ant.initialize(starts[i % len(starts)])
                ant.one_iteration(alpha, beta)
            self.graph.global_update_pheromone(rho)

            best_ant = None
            for ant in self.ants:
                ant.local_update_pheromone(d / n_ants)
                if ant.distance < min_distance:
                    min_distance = ant.distance
                    best_ant = ant
            if best_ant is not None:
                self.paths.append(best_ant.path)
                self.pheromones.append(self.graph.retrieve_pheromone())
                self.distances.append(min_distance)
                if verbose:
                    print('New best solution with d = {} !'.format(min_distance))

        return self.paths, self.distances

    def init_solution(self, alpha, beta):
        ant = Ant(self.graph)
        ant.initialize(0)
        ant.one_iteration(alpha, beta)
        return ant.distance


class Ant:
    def __init__(self, graph):
        self.position = None
        self.nodes_to_visit = []
        self.graph = graph
        self.distance = 0
        self.edges_visited = []
        self.path = []

    def initialize(self, start):
        self.position = start
        self.nodes_to_visit = [node.number for i, node in
                               enumerate(self.graph.nodes)
                               if i != self.position]
        self.distance = 0
        self.edges_visited = []
        self.path = [start]

    def one_iteration(self, alpha, beta):
        while self.nodes_to_visit:
            number = self.graph.select_node(self.position, self.nodes_to_visit,
                                            alpha, beta)
            self.nodes_to_visit.remove(number)
            self.path.append(number)
            self.edges_visited.append(
                self.graph.nodes_to_edge(self.position, number))
            self.distance += self.graph.nodes_to_edge(self.position,
                                                      number).distance
            self.position = number

    def local_update_pheromone(self, d):
        for edge in self.edges_visited:
            edge.pheromone += d / self.distance
