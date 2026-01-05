from abc import ABC, abstractmethod

from generator.graphs.types import GRAPH_STRATEGIES
from graph import DirectedGraph


class GeneratorStrategy(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def generate(self, num_nodes: int, num_edges: int) -> DirectedGraph:
        pass


def generator_factory(
    graph_strategy: GRAPH_STRATEGIES, num_nodes: int, num_edges: int
) -> GeneratorStrategy:

    if graph_strategy == GRAPH_STRATEGIES.barabasi_albert:
        from generator.graphs.albert_barabasi import AlbertBarabasiStrategy

        connectivity = max(1, num_edges // num_nodes)
        return AlbertBarabasiStrategy(num_nodes, connectivity)
    elif graph_strategy == GRAPH_STRATEGIES.random:
        raise ValueError(
            f"TO FIX: Random graph strategy not implemented yet. Implement inside generator/graphs/random.py"
        )
    else:
        raise ValueError(f"Unsupported graph strategy: {graph_strategy}")
