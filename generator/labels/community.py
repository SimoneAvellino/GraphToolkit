from generator.labels import LabelStrategy
import random

from graph import DirectedGraph
from networkx.algorithms.community import louvain_communities


class CommunityStrategy(LabelStrategy):
    """
    Assigns community-based labels to nodes and edges. It uses the Louvain method to detect communities.

    If the user provides node labels, they are assigned to communities in a round-robin fashion,
    otherwise communities are labeled with integers.

    If the user provides edge labels, they are assigned to communities in a round-robin fashion,
    otherwise edges connecting nodes within the same community are labeled "1" and edges connecting
    nodes from different communities are labeled "0".
    """

    def __init__(self):
        self._node_labels_assigned = set()
        self._edge_labels_assigned = set()

    def _get_node_label(self, node_labels: set[str], index: int) -> str:
        if len(node_labels) == 0:
            return str(index)
        remaining_labels = node_labels.difference(self._node_labels_assigned)
        if len(remaining_labels) > 0:
            label = random.choice(list(remaining_labels))
            self._node_labels_assigned.add(label)
            return label
        else:
            self._node_labels_assigned.clear()
            return self._get_node_label(node_labels, index)

    def _get_edge_label(self, edge_labels: set[str]) -> str:
        if len(edge_labels) == 0:
            return None
        remaining_labels = edge_labels.difference(self._edge_labels_assigned)
        if len(remaining_labels) > 0:
            label = random.choice(list(remaining_labels))
            self._edge_labels_assigned.add(label)
            return label
        else:
            self._edge_labels_assigned.clear()
            return self._get_edge_label(edge_labels)

    def assign(
        self, graph: DirectedGraph, node_labels: set[str], edge_labels: set[str]
    ):
        communities = louvain_communities(graph)
        for i, comm in enumerate(communities):
            # choose random node label from the provided list
            node_label = self._get_node_label(node_labels, i)
            for node in comm:
                graph.nodes[node]["label"] = f"{node_label}"

        for u, v, k in graph.edges(keys=True):
            edge_label = self._get_edge_label(edge_labels)
            if graph.nodes[u]["label"] == graph.nodes[v]["label"]:
                graph.edges[u, v, k]["label"] = (
                    edge_label if edge_label is not None else "1"
                )
            else:
                graph.edges[u, v, k]["label"] = (
                    edge_label if edge_label is not None else "0"
                )
