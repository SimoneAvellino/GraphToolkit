from generator.graphs.strategy import GeneratorStrategy
from graph import DirectedGraph
import networkx as nx


class AlbertBarabasiStrategy(GeneratorStrategy):

    def __init__(
        self,
        num_nodes: int,
        connectivity: int,
    ):
        """
        Parameters
        ----------
        num_nodes : int
            Number of nodes
        connectivity : int
            Number of edges to attach from a new node to existing nodes
        """
        super().__init__()
        self.num_nodes = num_nodes
        self.connectivity = connectivity

    def generate(self) -> DirectedGraph:
        g_simple = nx.barabasi_albert_graph(self.num_nodes, self.connectivity)
        g_multi = nx.MultiGraph(g_simple)
        return g_multi
