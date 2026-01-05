from abc import ABC, abstractmethod
from graph import DBGraph, DirectedGraph
from reify.types import ReifyStrategyTypes


class ReifyStrategy(ABC):

    @abstractmethod
    def reify(self, graph: DBGraph) -> DBGraph:
        """
        Reify the given graph according to the strategy.
        """
        pass


def reify_strategy_factory(strategy_type: str) -> ReifyStrategy:
    """
    Factory function to create a reification strategy based on the given type.
    """
    if strategy_type == ReifyStrategyTypes.multi_arcs_expansion:
        from reify.multi_arcs_expansion import MultiArcsExpansionStrategy

        return MultiArcsExpansionStrategy()
    else:
        raise ValueError(f"Unknown reification strategy type: {strategy_type}")
