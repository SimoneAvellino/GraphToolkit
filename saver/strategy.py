from abc import ABC, abstractmethod

from db import DBGraphs
from graph import DirectedGraph
from saver.types import OutputFormat


class SaverStrategy(ABC):

    @abstractmethod
    def save(self, graph: DirectedGraph, output_path: str):
        pass

    @abstractmethod
    def format_extension(self) -> str:
        pass

    @abstractmethod
    def save_db(self, graphs: DBGraphs, output_path: str, append: bool = False):
        pass


def saver_factory_strategy(format: OutputFormat) -> SaverStrategy:
    if format == OutputFormat.data:
        from saver.data import DataSaverStrategy

        return DataSaverStrategy()
    else:
        raise ValueError(f"Unsupported format: {format}")
