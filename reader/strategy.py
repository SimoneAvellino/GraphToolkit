from abc import ABC, abstractmethod

from db import DBGraphs
from graph import DirectedGraph
from reader.types import InputFormat


class GraphReaderStrategy(ABC):

    @abstractmethod
    def read(self, path: str) -> DirectedGraph:
        raise NotImplementedError("Subclasses should implement this method")

    def read_db(self, path: str) -> DBGraphs:
        raise NotImplementedError("Subclasses should implement this method")


def reader_factory_strategy(format: InputFormat) -> GraphReaderStrategy:
    if format == InputFormat.csv:
        from reader.csv import CSVGraphReader

        return CSVGraphReader()
    elif format == InputFormat.data:
        from reader.data import DataGraphReader

        return DataGraphReader()
    else:
        raise ValueError(f"Unsupported format: {format}")
