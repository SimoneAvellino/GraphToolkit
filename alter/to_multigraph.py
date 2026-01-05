from alter.strategy import AlterStrategy
from graph import DBGraph, DirectedGraph
import random


class ToMultigraph(AlterStrategy):

    def __init__(
        self,
        K: int | tuple[int],
        assign_probability: float = 0.5,
        edges_labels_strategy: str = "dummy",  # TODO: implement different strategies
    ):
        """Assign multiple edges between nodes to convert a graph into a multigraph.

        Args:
            K (int | tuple[int], optional): _description_. Defaults to 2.
            assign_probability (float, optional): _description_. Defaults to 0.5.
            edges_labels_strategy (str): Strategy to assign labels to new edges. Defaults to "dummy". It assign the label "extra_[existinglabel]".

        Raises:
            ValueError: K must be an int or a tuple of two ints
        """
        if type(K) is int:
            self.K = (K, K)
        elif type(K) is tuple and len(K) == 2:
            self.K = K
        else:
            raise ValueError("K must be an int or a tuple of two ints")
        self.assign_probability = assign_probability
        self.edges_labels_strategy = edges_labels_strategy

    def alter(self, graph: DBGraph) -> DBGraph:
        """
        Alter the given graph to convert it into a multigraph.

        Parameters:
        graph (DirectedGraph): The input directed graph to be altered.
        Returns:
        DirectedGraph: The altered multigraph.
        """
        multi_g = graph.copy()
        for u, v, data in graph.edges(data=True):
            rand = random.random()
            if rand > self.assign_probability:
                continue
            K = random.randint(self.K[0], self.K[1])
            for _ in range(K):
                multi_g.add_edge(u, v, label=f"extra_{data['label']}")

        return multi_g

    def what_changed(self, original_graph: DBGraph, altered_graph: DBGraph) -> str:
        original_edge_count = original_graph.number_of_edges()
        altered_edge_count = altered_graph.number_of_edges()
        added_edges = altered_edge_count - original_edge_count
        return (
            f"Converted to multigraph by adding {added_edges} edges "
            f"(from {original_edge_count} to {altered_edge_count} edges)."
        )
