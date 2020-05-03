import streamlit as st
import pydeck
import pandas as pd


class MapPlotter:
    def __init__(self, graph):
        self.graph = graph
        self.r = None
        self.layer_pheromones = None
        self.layer_best_path = None
        self.chart = None
        self.text = None
        self.df_distance = None
        self.distance_chart = None

    def plot_graph(self):
        data = []
        for edge in self.graph._nodes_to_edge.values():
            node1 = edge.node1
            node2 = edge.node2
            data.append({
                "start": [node1.x, node1.y],
                "end": [node2.x, node2.y],
            })
        lat = [line["start"][1] for line in data]
        lng = [line["start"][0] for line in data]
        center_lat = (max(lat) - min(lat)) / 2 + min(lat)
        center_lng = (max(lng) - min(lng)) / 2 + min(lng)

        layer = pydeck.Layer(
            "LineLayer",
            data,
            get_source_position="start",
            get_target_position="end",
            coverage=1,
            pickable=True,
        )
        initial_view_state = pydeck.ViewState(latitude=center_lat, longitude=center_lng, zoom=2.8, max_zoom=10, pitch=0, bearing=0)
        r = pydeck.Deck(layers=[layer], initial_view_state=initial_view_state, map_style="", tooltip=True, mapbox_key="")
        st.pydeck_chart(r)

    def init_plot(self):

        data = []
        for edge in self.graph._nodes_to_edge.values():
            node1 = edge.node1
            node2 = edge.node2
            data.append({
                "start": [node1.x, node1.y],
                "end": [node2.x, node2.y],
                "value": 1,
            })
        lat = [line["start"][1] for line in data]
        lng = [line["start"][0] for line in data]
        center_lat = (max(lat) - min(lat)) / 2 + min(lat)
        center_lng = (max(lng) - min(lng)) / 2 + min(lng)

        self.layer_pheromones = pydeck.Layer(
            "LineLayer",
            data,
            get_source_position="start",
            get_target_position="end",
            get_width="value",
            coverage=1,
            pickable=True,
        )
        best = []
        self.layer_best_path = pydeck.Layer(
            "LineLayer",
            best,
            get_source_position="start",
            get_target_position="end",
            get_color=[255, 0, 0],
            coverage=1,
            pickable=True,
        )
        initial_view_state = pydeck.ViewState(latitude=center_lat, longitude=center_lng, zoom=2.8, max_zoom=10, pitch=0, bearing=0)
        self.r = pydeck.Deck(layers=[self.layer_pheromones, self.layer_best_path], initial_view_state=initial_view_state, map_style="", tooltip=True, mapbox_key="")
        self.chart = st.pydeck_chart(self.r)
        self.df_distance = pd.DataFrame({"distance": []})
        self.distance_chart = st.line_chart(self.df_distance)
        self.text = st.empty()

    def update(self, pheromones, best_path, distance):
        data = []
        for k, value in pheromones.items():
            node1 = self.graph._nodes_to_edge[k].node1
            node2 = self.graph._nodes_to_edge[k].node2
            data.append({
                "start": [node1.x, node1.y],
                "end": [node2.x, node2.y],
                "value": value,
            })
        best = []
        start = [self.graph.nodes[best_path[0]].x, self.graph.nodes[best_path[0]].y]
        for number in best_path:
            best.append({
                "start": start,
                "end": [self.graph.nodes[number].x, self.graph.nodes[number].y]
            })
            start = [self.graph.nodes[number].x, self.graph.nodes[number].y]

        self.layer_pheromones.data = data
        self.layer_best_path.data = best
        self.r.update()
        self.chart.pydeck_chart(self.r)
        self.distance_chart.add_rows({"distance": [distance]})
        self.text.text(f"Best distance = {distance:.2f}")
