from operator import le
from db import DBGraphs
from graph import DBGraph, DirectedGraph
from reader.strategy import GraphReaderStrategy


class DataGraphReader(GraphReaderStrategy):

    def _line_is_graph_header(self, line: str) -> bool:
        return line.startswith("t #")

    def _line_is_node(self, line: str) -> bool:
        return line.startswith("v ")

    def _line_is_edge(self, line: str) -> bool:
        return line.startswith("e ")

    def _extract_graph_id(self, line: str) -> int:
        parts = line.strip().split()
        if len(parts) >= 3 and parts[0] == "t" and parts[1] == "#":
            return parts[2]
        else:
            raise ValueError("Invalid graph header line format")

    def _extract_node(self, line: str) -> tuple[int, str]:
        parts = line.strip().split()
        if len(parts) >= 2 and parts[0] == "v":
            node_id = int(parts[1])
            if len(parts) > 2:
                labels = parts[2:]
            else:
                labels = []
            return node_id, labels
        else:
            raise ValueError("Invalid node line format")

    def _extract_edge(self, line: str) -> tuple[int, int, str]:
        parts = line.strip().split()
        if parts[0] == "e" and len(parts) >= 3:
            src_id = int(parts[1])
            dst_id = int(parts[2])
            if len(parts) > 3:
                labels = parts[3:]
            else:
                labels = []
            return src_id, dst_id, labels
        else:
            raise ValueError("Invalid edge line format")

    def read_db(self, path: str) -> DBGraphs:
        # read the file
        db = DBGraphs()
        with open(path, "r") as file:
            lines = file.readlines()
            graph = DBGraph()
            for l in lines:
                if self._line_is_graph_header(l):
                    # process the graph header
                    graph_id = self._extract_graph_id(l)
                    graph = DBGraph(graph_id=graph_id)
                    db.add_graph(graph)
                elif self._line_is_node(l):
                    node_id, labels = self._extract_node(l)
                    graph.add_node(node_id, labels=labels)
                elif self._line_is_edge(l):
                    src_id, dst_id, labels = self._extract_edge(l)
                    if len(labels) == 0:
                        graph.add_edge(src_id, dst_id)
                    for label in labels:
                        graph.add_edge(src_id, dst_id, label=label)

        return db

    def read(self, path: str) -> DirectedGraph:
        # read the file
        graph = DirectedGraph()
        with open(path, "r") as file:
            lines = file.readlines()
            for l in lines:
                if self._line_is_node(l):
                    node_id, labels = self._extract_node(l)
                    graph.add_node(node_id, labels=labels)
                elif self._line_is_edge(l):
                    src_id, dst_id, labels = self._extract_edge(l)
                    for label in labels:
                        graph.add_edge(src_id, dst_id, label=label)

        return graph
