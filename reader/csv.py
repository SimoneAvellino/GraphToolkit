import os
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import networkx as nx
from dataclasses import dataclass, field

from db import Graph
from graph import DirectedGraph
from reader.strategy import GraphReaderStrategy


@dataclass
class CSVNode:
    df: pd.DataFrame
    label: str


@dataclass
class CSVEdge:
    df: pd.DataFrame
    label: str


@dataclass
class CSVGraph:
    nodes: list[CSVNode] = field(default_factory=list)
    edges: list[CSVEdge] = field(default_factory=list)


class CSVGraphReader(GraphReaderStrategy):

    def _read_csv_graph(self, folder_path):
        graph = CSVGraph()

        def load_csv(file_name):
            file_path = os.path.join(folder_path, file_name)
            label = file_name[:-4]  # remove .csv extension
            df = pd.read_csv(file_path)
            self._is_valid_df(df)
            if self._is_node_df(df):
                return CSVNode(df=df, label=label)
            if self._is_edge_df(df):
                return CSVEdge(df=df, label=label)
            return None

        csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
        with ThreadPoolExecutor() as executor:
            for result in executor.map(load_csv, csv_files):
                if isinstance(result, CSVNode):
                    graph.nodes.append(result)
                elif isinstance(result, CSVEdge):
                    graph.edges.append(result)
        return graph

    def _is_valid_df(self, df):
        if len(df.columns) != 1:
            raise ValueError("DataFrame must have exactly one column")
        if len(df) == 0:
            raise ValueError("DataFrame must have at least one row")
        return True

    def _is_node_df(self, df):
        # TODO: parametrize the logic to identify node dataframes
        return "id:ID" in df.columns[0]

    def _is_edge_df(self, df):
        # TODO: parametrize the logic to identify edge dataframes
        return ":START_ID" in df.columns[0]

    def _extract_node_entity(self, header_name: str) -> str:
        # Assuming format like "id:ID(EntityType)"
        if "(" in header_name and ")" in header_name:
            return header_name.split("(")[1].split(")")[0]
        return "Unknown"

    def _extract_edge_entities(self, header_name: str) -> tuple[str, str]:
        # Assuming format like ":START_ID(Person)|:END_ID(Person)"
        if "|" in header_name:
            parts = header_name.split("|")
            start_entity = parts[0].split("(")[1].split(")")[0]
            end_entity = parts[1].split("(")[1].split(")")[0]
            return start_entity, end_entity
        return "Unknown", "Unknown"

    def _extract_src_dst_from_edge_row(self, edge_str) -> tuple[int, int]:
        # supposing format like "src_id|dst_id"
        parts = edge_str.split("|")
        if len(parts) != 2:
            raise ValueError("Edge string must be in the format 'src_id|dst_id'")
        return int(parts[0]), int(parts[1])

    def _csv_to_nx(self, csv_graph: CSVGraph) -> DirectedGraph:
        G = nx.MultiDiGraph()

        for node in csv_graph.nodes:
            node_id_column = node.df.columns[0]
            for node_id in node.df[node_id_column].tolist():
                G.add_node(node_id, label=node.label)

        for edge in csv_graph.edges:
            for row in edge.df.itertuples(index=False, name=None):
                edge_value = row[0]
                src, dst = self._extract_src_dst_from_edge_row(edge_value)
                # let networkx handle multi-edge keys automatically
                G.add_edge(src, dst, label=edge.label)

        return DirectedGraph(G)

    def read(self, folder_path) -> DirectedGraph:
        csv_graph = self._read_csv_graph(folder_path)
        return self._csv_to_nx(csv_graph)
