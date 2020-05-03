import numpy as np


class ACO:
    def __init__(self, graph):
        self.graph = graph
        self.ants = []
        self.paths = []
        self.pheromones = []
        self.distances = []

    def solve(self, alpha=1, beta=1, rho=0.1, n_ants=20, n_iterations=10, verbose=False, plotter=None):
        d = self.init_solution(alpha, beta)
        # TODO compute mean
        d_mean = d / (len(self.graph.nodes))
        min_distance = np.inf
        self.ants = []
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

            best_ant = None
            for ant in self.ants:
                ant.local_update_pheromone(d / n_ants)
                if ant.distance < min_distance:
                    min_distance = ant.distance
                    best_ant = ant
            if best_ant is not None:
                self.paths.append(best_ant.path)
                if verbose:
                    print('New best solution with d = {:.2f} !'.format(min_distance))
            else:
                self.paths.append(self.paths[-1])
            self.pheromones.append(self.graph.retrieve_pheromone())
            self.distances.append(min_distance)
            if plotter is not None:
                plotter.update(self.pheromones[-1], self.paths[-1], min_distance)

        return self.paths, self.distances

    def init_solution(self, alpha, beta):
        ant = Ant(self.graph)
        ant.initialize(0)
        ant.one_iteration(alpha, beta)
        return ant.distance


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
            node_index = self.graph.select_node(self.position, self.nodes_to_visit,
                                                alpha, beta, self.d_mean)
            self.nodes_to_visit.remove(node_index)
            self.path.append(node_index)
            self.edges_visited.append(
                self.graph.nodes_to_edge(self.position, node_index))
            self.distance += self.graph.nodes_to_edge(self.position,
                                                      node_index).distance
            self.position = node_index
        self.path.append(self.path[0])
        self.distance += self.graph.nodes_to_edge(self.position,
                                                  self.path[0]).distance

    def local_update_pheromone(self, d):
        for edge in self.edges_visited:
            edge.pheromone += d / self.distance
