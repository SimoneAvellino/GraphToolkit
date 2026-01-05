from fileinput import filename
from db import DBGraphs
from graph import DirectedGraph
from saver.strategy import saver_factory_strategy, SaverStrategy
import os


class Saver:

    __DEFAULT_FILE_NAME = "output"

    def __init__(self, strategy: SaverStrategy):
        self._strategy = strategy

    def _construct_path(self, given_path: str) -> str:
        ext = self._strategy.format_extension()
        if os.path.isdir(given_path):
            return os.path.join(given_path, f"{self.__DEFAULT_FILE_NAME}.{ext}")
        else:
            abs_path = os.path.abspath(given_path)
            # remove possible extension because is appended automatically
            abs_path = os.path.splitext(abs_path)[0]
            return f"{abs_path}.{ext}"

    def save(self, graph: DirectedGraph, output_path: str):
        """
        Save a single graph to the given output path using the strategy
        """
        output_path = self._construct_path(output_path)
        self._strategy.save(graph, output_path)

    def save_db(self, graphs: DBGraphs, output_path: str, append: bool = False):
        """
        Save a database of graphs to the given output path using the strategy.
        """
        output_path = self._construct_path(output_path)
        self._strategy.save_db(graphs, output_path, append=append)


def saver_factory(output_format) -> Saver:
    save_strategy = saver_factory_strategy(output_format)
    saver = Saver(save_strategy)
    return saver
