import numpy as np
import matplotlib.pyplot as plt

from solver.graph import Node, Graph
from solver.aco import ACO


def main():
    # # Simple example

    # Create and plot the graph
    n_nodes = 30

    np.random.seed(0)
    coordinates = np.random.rand(n_nodes, 2) * 10

    nodes = []
    for i in range(n_nodes):
        nodes.append(Node(coordinates[i, 0], coordinates[i, 1]))

    graph = Graph(nodes)
    fig, ax = graph.plot_graph()
    plt.show()

    # Solve for 100 iterations
    aco = ACO(nodes)
    paths, distances = aco.solve(rho=0.5, n_iterations=100, verbose=True)

    # Plot results
    anim = graph.plot_paths(paths, aco.pheromones, distances)
    plt.show()


if __name__ == '__main__':
    main()
