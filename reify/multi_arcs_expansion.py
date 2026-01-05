from graph import DBGraph, DirectedGraph
from reify.strategy import ReifyStrategy


class MultiArcsExpansionStrategy(ReifyStrategy):

    def __init__(
        self,
        source_label: str = "__source__",
        target_label: str = "__target__",
        new_node_prefix: str = "__edge_",
    ):
        """
        Given a multigraph, for each pair of nodes with multiple arcs between them,
        expand the arcs into separate nodes and connect them with single arcs.

        Given A, B nodes and e1, e2, ..., en multiple edges between them,
        create new nodes N1, N2, ..., Nn and connect them as follows:

        A -->N1--> B the label of the edge A --> N1 is "__source__" and the label of the edge N1 --> B  is "__target__"

        A -->N2--> B the label of the edge A --> N2 is "__source__" and the label of the edge N2 --> B is "__target__"

        ...

        A -->Nn--> B the label of the edge A --> Nn is "__source__" and the label of the edge Nn --> B is "__target__"

        The label of the nodes N1, N2, ..., Nn are created with the prefix specified in new_node_prefix concatenated with their current label.

        Parameters
        ----------
        source_label : str
            The label to assign to the new edges originating from the source node.
        target_label : str
            The label to assign to the new edges pointing to the target node.
        new_node_prefix : str
            The prefix to use for naming the new intermediate nodes.
        """
        super().__init__()
        self.source_label = source_label
        self.target_label = target_label
        self.new_node_prefix = new_node_prefix

    def reify(self, graph: DBGraph) -> DBGraph:

        reif_g = graph.copy()

        max_node_id = max(graph.nodes(), default=-1)

        for u, v in set(graph.edges()):
            count = graph.number_of_edges(u, v)
            if count == 1:
                data = graph.get_edge_data(u, v)[0]
                reif_g.add_edge(u, v, **data)
            else:
                keys = list(graph.get_edge_data(u, v).keys())
                for i, key in enumerate(keys):
                    edge_data = graph.get_edge_data(u, v, key)
                    new_node_id = max_node_id + 1
                    max_node_id += 1
                    new_node_label = edge_data.get("label", "")
                    reif_g.add_node(
                        new_node_id, labels=f"{self.new_node_prefix}{new_node_label}"
                    )
                    reif_g.add_edge(u, new_node_id, label=self.source_label)
                    reif_g.add_edge(new_node_id, v, label=self.target_label)
        return reif_g
