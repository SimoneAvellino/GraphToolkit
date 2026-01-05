from enum import Enum


class GraphStrategyName(str, Enum):
    random = "random"
    barabasi_albert = "barabasi_albert"


GRAPH_STRATEGIES = GraphStrategyName
