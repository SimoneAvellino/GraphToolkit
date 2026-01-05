import networkx as nx
from typing import Union

from graph import DBGraph

Graph = nx.MultiDiGraph


class DBGraphs:

    def __init__(self, graphs: list[DBGraph] | None = None):
        # Use a fresh list per instance to avoid shared state across DBGraphs objects
        self.graphs = list(graphs) if graphs is not None else []

    def add_graph(self, graph: DBGraph):
        self.graphs.append(graph)

    def get_graphs(self) -> list[DBGraph]:
        return self.graphs

    def print_stats(self):
        for i, g in enumerate(self.graphs):
            print(
                f"Graph {i}: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges"
            )

        # Mean number of nodes and edges
        total_nodes = sum(g.number_of_nodes() for g in self.graphs)
        total_edges = sum(g.number_of_edges() for g in self.graphs)
        mean_nodes = total_nodes / len(self.graphs) if self.graphs else 0
        mean_edges = total_edges / len(self.graphs) if self.graphs else 0

        # std number of nodes and edges
        std_nodes = (
            sum((g.number_of_nodes() - mean_nodes) ** 2 for g in self.graphs)
            / len(self.graphs)
            if self.graphs
            else 0
        ) ** 0.5
        std_edges = (
            sum((g.number_of_edges() - mean_edges) ** 2 for g in self.graphs)
            / len(self.graphs)
            if self.graphs
            else 0
        ) ** 0.5
        print("Overall statistics:")
        print("- Total graphs:", len(self.graphs))
        print("- Total nodes:", total_nodes, "Mean:", mean_nodes, "Std:", std_nodes)
        print("- Total edges:", total_edges, "Mean:", mean_edges, "Std:", std_edges)
