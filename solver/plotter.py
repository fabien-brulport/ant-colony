import time

import streamlit as st
import pydeck
import pandas as pd


class MapPlotter:
    def __init__(self, graph, zoom=3.):
        self.graph = graph
        self.zoom = zoom
        self.r = None
        self.layer_pheromones = None
        self.layer_best_path = None
        self.chart = None
        self.text = None
        self.df_distance = None
        self.distance_chart = None

    def init_plot(self):

        # Layer which shows the nodes name (if they exist)
        nodes_name = []
        for node in self.graph.nodes.values():
            nodes_name.append({
                "coordinates": [node.x, node.y],
                "name": node.name,
            })
        layer_nodes = pydeck.Layer(
            "ScatterplotLayer",
            nodes_name,
            coverage=1,
            pickable=True,
            get_position="coordinates",
            radius_min_pixels=4,
            get_color=[0, 166, 251],
        )

        # Layer which shows the value of pheromones
        lines_pheromones = self._get_lines_pheromones()
        self.layer_pheromones = pydeck.Layer(
            "LineLayer",
            lines_pheromones,
            get_source_position="start",
            get_target_position="end",
            get_width="value",
            width_scale=4,
            coverage=1,
            pickable=True,
        )

        # Layer which shows the best path in red
        self.layer_best_path = pydeck.Layer(
            "LineLayer",
            [],  # empty layer
            get_source_position="start",
            get_target_position="end",
            get_color=[255, 0, 0],
            coverage=1,
            width_scale=3,
            pickable=True,
        )
        initial_view_state = self._get_init_view(lines_pheromones)
        self.r = pydeck.Deck(layers=[layer_nodes, self.layer_pheromones, self.layer_best_path], initial_view_state=initial_view_state, map_style="", tooltip=True, mapbox_key="")
        self.chart = st.pydeck_chart(self.r)

        # Empty plot to show the distance convergence
        self.df_distance = pd.DataFrame({"Best distance": []})
        self.distance_chart = st.line_chart(self.df_distance)
        self.text = st.empty()

    def update(self, best_path, distance):
        lines_pheromones = self._get_lines_pheromones()
        lines_best_path = []
        start = [best_path[0].x, best_path[0].y]
        for node in best_path:
            lines_best_path.append({
                "start": start,
                "end": [node.x, node.y]
            })
            start = [node.x, node.y]

        self.layer_pheromones.data = lines_pheromones
        self.layer_best_path.data = lines_best_path
        self.r.update()
        self.chart.pydeck_chart(self.r)
        self.distance_chart.add_rows({"Best distance": [distance]})
        self.text.text(f"Best distance = {distance:.2f}")
        time.sleep(0.01)

    def _get_init_view(self, lines):
        lat = [line["start"][1] for line in lines]
        lng = [line["start"][0] for line in lines]
        center_lat = (max(lat) - min(lat)) / 2 + min(lat)
        center_lng = (max(lng) - min(lng)) / 2 + min(lng)
        return pydeck.ViewState(latitude=center_lat, longitude=center_lng, zoom=self.zoom, max_zoom=10, pitch=0, bearing=0)

    def _get_lines_pheromones(self):
        lines_pheromones = []
        for (node_index_1, node_index_2), value in self.graph.retrieve_pheromone().items():
            node1 = self.graph.nodes[node_index_1]
            node2 = self.graph.nodes[node_index_2]
            lines_pheromones.append({
                "start": [node1.x, node1.y],
                "end": [node2.x, node2.y],
                "value": value,
            })
        return lines_pheromones
