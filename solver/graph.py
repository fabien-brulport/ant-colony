import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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
        self.distance = ((self.node1.x - self.node2.x) ** 2 + (
            self.node1.y - self.node2.y) ** 2) ** 0.5
        self.pheromone = 1

    def value(self, alpha, beta, d_mean):
        # print(self.pheromone**alpha, (1/self.distance)**beta)
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

    def plot_graph(self):
        fig, ax = plt.subplots()

        plt.scatter([node.x for node in self.nodes],
                    [node.y for node in self.nodes], c='r', marker='x')

        for edge in self._nodes_to_edge.values():
            plt.plot([edge.node1.x, edge.node2.x], [edge.node1.y, edge.node2.y],
                     'k', alpha=0.3)

        return fig, ax

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
            number = mapping[np.random.choice(
                np.random.choice(len(probabilities), 1000, p=probabilities))]
            return number

    def global_update_pheromone(self, rho):
        for edge in self._nodes_to_edge.values():
            edge.pheromone = (1 - rho) * edge.pheromone

    def retrieve_pheromone(self):
        pheromones = dict()
        for k, edge in self._nodes_to_edge.items():
            pheromones[k] = edge.pheromone

        return pheromones

    def plot_paths(self, paths, pheromones, distances, fig=None):
        if fig is None:
            fig, axs = plt.subplots(1, 2)
        else:
            axs = fig.get_axes()

        # Edges
        ax = axs[0]
        edges = []
        for k, value in pheromones[0].items():
            node1 = self._nodes_to_edge[k].node1
            node2 = self._nodes_to_edge[k].node2
            x = [node1.x, node2.x]
            y = [node1.y, node2.y]
            color = (max(0, 0.9 - value))
            line, = ax.plot(x, y, lw=4, color=str(color))
            edges.append(line)

        # Best paths
        x_best = [[self.nodes[number].x for number in path] for path in paths]
        y_best = [[self.nodes[number].y for number in path] for path in paths]
        best_path, = ax.plot(x_best[0], y_best[0], color='r', lw=2)

        # Convergence
        ax = axs[1]
        ax.plot(distances)
        frac_x = 0.05 * len(distances)
        frac_y = 0.05 * (max(distances) - min(distances))
        point = ax.scatter(0, distances[0], marker='o')
        text = ax.annotate('', xy=(0 + frac_x, distances[0] + frac_y),
                           bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

        def animate(i):
            for j, value in enumerate(pheromones[i].values()):
                color = (max(0, 1 - value))
                edges[j].set_color(str(color))
                edges[j].set_linewidth(value)

            best_path.set_data(x_best[i], y_best[i])
            point.set_offsets([i, distances[i]])
            text.set_text("d = {:.3f}".format(distances[i]))
            text.set_position([i + frac_x, distances[i] + frac_y])

            return edges, best_path, point, text,

        anim = animation.FuncAnimation(fig, animate, frames=len(paths), interval=100, blit=False)
        return anim
