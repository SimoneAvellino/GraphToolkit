from db import DBGraphs
from graph import DirectedGraph
from saver.strategy import SaverStrategy


class DataSaverStrategy(SaverStrategy):

    def _to_data_string(self, graph: DirectedGraph) -> str:
        """
        Convert a Graph object to a data string representation

        example:

        v 0 label1, label2
        v 1 label2
        e 0 1 labelA, labelB
        e 1 0 labelA
        """
        res = ""
        for node_id, node_data in graph.nodes(data=True):
            labels = node_data.get("labels", [])
            if isinstance(labels, str):
                labels = [labels]
            labels_str = ", ".join(labels)
            res += f"v {node_id} {labels_str}\n"
        for src, dst, edge_data in graph.edges(data=True):
            labels = edge_data.get("label", [])
            if isinstance(labels, str):
                labels = [labels]
            labels_str = ", ".join(labels)
            res += f"e {src} {dst} {labels_str}\n"
        return res

    def save(self, graph: DirectedGraph, output_path: str) -> None:
        """
        Convert a Graph object to a data file representation and save it to output_path
        """
        data_string = self._to_data_string(graph)
        with open(output_path, "w") as f:
            f.write(data_string)

    def save_db(self, db: DBGraphs, output_path: str, append: bool = False) -> None:
        """
        Save a database of graphs to a data file representation and save it to output_path
        Each graph has a starting line "t # [graph_index]"

        Parameters:
            graphs: list of DirectedGraph objects to save
            output_path: path to the output file
            append: whether to append to the file (if True) or overwrite (if False)
        """
        mode = "a" if append else "w"
        with open(output_path, mode) as f:
            for graph in db.get_graphs():
                f.write(f"t # {graph.get_graph_id()}\n")
                data_string = self._to_data_string(graph)
                f.write(data_string)

    def format_extension(self) -> str:
        return "data"
