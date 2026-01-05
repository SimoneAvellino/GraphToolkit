from alter.strategy import AlterStrategy
from graph import DBGraph, DirectedGraph


class GraphAlter:

    def __init__(self, strategy: AlterStrategy):
        self.strategy = strategy

    def alter(self, graph: DBGraph) -> DBGraph:
        return self.strategy.alter(graph)

    def what_changed(self, original_graph: DBGraph, altered_graph: DBGraph) -> str:
        return self.strategy.what_changed(original_graph, altered_graph)
