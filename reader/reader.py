from db import DBGraphs
from graph import DirectedGraph
from reader.strategy import GraphReaderStrategy, reader_factory_strategy
from reader.types import InputFormat


class Reader:

    def __init__(self, strategy: GraphReaderStrategy):
        self._strategy = strategy

    def read(self, path: str) -> DirectedGraph:
        return self._strategy.read(path)

    def read_db(self, path: str) -> DBGraphs:
        return self._strategy.read_db(path)


def reader_factory(input_format: InputFormat) -> Reader:

    read_strategy = reader_factory_strategy(input_format)
    reader = Reader(read_strategy)
    return reader
