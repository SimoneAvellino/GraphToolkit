from abc import ABC, abstractmethod

from graph import DBGraph, DirectedGraph


class AlterStrategy(ABC):
    @abstractmethod
    def alter(self, graph: DirectedGraph) -> DirectedGraph:
        """Apply the alteration strategy to the graph."""
        raise NotImplementedError

    @abstractmethod
    def what_changed(self, original_graph: DBGraph, altered_graph: DBGraph) -> str:
        """Describe what changed between the original and altered graph."""
        raise NotImplementedError


def alter_strategy_factory(strategy_type: str) -> AlterStrategy:
    """
    Factory function to create an alteration strategy based on the given type.
    """
    if strategy_type == "to_multigraph":
        from alter.to_multigraph import ToMultigraph

        return ToMultigraph(K=(2, 2), assign_probability=0.2)
    else:
        raise ValueError(f"Unknown alteration strategy type: {strategy_type}")
