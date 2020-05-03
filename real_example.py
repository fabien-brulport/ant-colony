import streamlit as st
import pandas as pd

from solver.graph import Node, Graph
from solver.aco import ACO
from solver.plotter import MapPlotter


def main():
    n_ants = st.sidebar.slider("Number of ants", 1, 100, 20)
    n_iter = st.sidebar.slider("Number of iteration", 1, 200, 100)
    alpha = st.sidebar.slider("alpha (pheromone weight)", 0., 10., 1.)
    beta = st.sidebar.slider("beta (heuristic weight)", 0., 10., 1.)
    rho = st.sidebar.slider("rho (evaporation rate)", 0., 1., 0.5)

    df = pd.read_csv("data/european_cities.csv")
    cities = df["name"]
    longitudes = df["lng"]
    latitudes = df["lat"]

    # Create the graph
    nodes = []
    for i in range(len(cities)):
        nodes.append(Node(longitudes[i], latitudes[i]))

    graph = Graph(nodes)
    st.title("European cities")
    plotter = MapPlotter(graph)
    # plotter.plot_graph()
    plotter.init_plot()

    # Solve for 100 iterations
    aco = ACO(nodes)
    paths, distances = aco.solve(
        alpha=alpha,
        beta=beta,
        rho=rho,
        n_ants=n_ants,
        n_iterations=n_iter,
        plotter=plotter,
    )


if __name__ == '__main__':
    main()
