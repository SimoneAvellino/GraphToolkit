from graph import DBGraph, DirectedGraph
from reify.multi_arcs_expansion import MultiArcsExpansionStrategy
from reify.strategy import ReifyStrategy
import enum


class Reificator:

    def __init__(self, strategy: ReifyStrategy):
        self._strategy = strategy

    def reify(self, graph: DBGraph) -> DBGraph:
        """
        Reify the given graph using the injected strategy.
        """
        return self._strategy.reify(graph)
