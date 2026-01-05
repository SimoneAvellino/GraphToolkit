from generator.labels import LabelStrategy
from graph import DirectedGraph
import random


class RandomStrategy(LabelStrategy):
    """
    Assigns random labels to nodes and edges from the provided label lists.
    """

    def assign(
        self, graph: DirectedGraph, node_labels: set[str], edge_labels: set[str]
    ):
        self.assign_random_node_labels(graph, node_labels)
        self.assign_random_edge_labels(graph, edge_labels)

    def assign_random_node_labels(
        self, graph: DirectedGraph, node_labels: set[str]
    ) -> None:
        for node in graph.nodes():
            label = random.choice(list(node_labels))
            graph.nodes[node]["label"] = label

    def assign_random_edge_labels(
        self, graph: DirectedGraph, edge_labels: set[str]
    ) -> None:
        for u, v, key in graph.edges(keys=True):
            label = random.choice(list(edge_labels))
            graph.edges[u, v, key]["label"] = label
