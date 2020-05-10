import numpy as np
import streamlit as st

from solver.graph import Node, Graph
from solver.aco import ACO


def main():
    # # Simple example
    st.title("Synthetic example")

    # Create and plot the graph
    st.write("Create a graph with 30 nodes. Each node has a position (x, y) between 0 and 10.")
    n_nodes = 30

    np.random.seed(0)
    coordinates = np.random.rand(n_nodes, 2) * 10

    nodes = []
    for i in range(n_nodes):
        nodes.append(Node(coordinates[i, 0], coordinates[i, 1]))

    graph = Graph(nodes)

    # Solve for 100 iterations
    aco = ACO(nodes)
    paths, distances = aco.solve(rho=0.5, n_iterations=100, verbose=True)


if __name__ == '__main__':
    main()
