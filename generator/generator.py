from dataclasses import dataclass
from abc import ABC, abstractmethod
import networkx as nx
from db import Graph
import json

from generator.graphs.strategy import GeneratorStrategy
from generator.labels.strategy import LabelStrategy


class GraphGenerator:

    def __init__(
        self, graph_strategy: GeneratorStrategy, label_strategy: LabelStrategy
    ):
        self.graph_strategy = graph_strategy
        self.label_strategy = label_strategy

    def generate(self) -> Graph:
        graph = self.graph_strategy.generate()
        graph = self.label_strategy.assign(graph)
        return graph
