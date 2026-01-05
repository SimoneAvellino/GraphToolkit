from graph import DirectedGraph
from .strategy import LabelStrategy


class NoneLabelStrategy(LabelStrategy):

    def assign(self, graph) -> DirectedGraph:
        return graph
