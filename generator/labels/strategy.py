from abc import ABC, abstractmethod

from generator.labels.types import LabelStrategyName
from graph import DirectedGraph


class LabelStrategy(ABC):

    @abstractmethod
    def assign(self, graph: DirectedGraph) -> DirectedGraph:
        pass


def label_factory(label_strategy: LabelStrategyName) -> LabelStrategy:

    if label_strategy == LabelStrategyName.none:
        from generator.labels.none import NoneLabelStrategy

        return NoneLabelStrategy()
    elif label_strategy == LabelStrategyName.random:
        from generator.labels.random import RandomLabelStrategy

        return RandomLabelStrategy()
    elif label_strategy == LabelStrategyName.community:
        from generator.labels.community import CommunityLabelStrategy

        return CommunityLabelStrategy()
    else:
        raise ValueError(f"Unsupported label strategy: {label_strategy}")
