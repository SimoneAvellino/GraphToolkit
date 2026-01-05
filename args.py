from argparse import ArgumentParser
from cProfile import label
from dataclasses import dataclass
import re
from saver import SaveFormat


@dataclass
class MainArgs:
    num_nodes: int | list[int]
    num_edges: int | list[int]
    output_dir: str
    num_graphs: int
    generation_strategy: str
    save_format: SaveFormat
    labels: str | None
    labels_strategy: str


def parse_args():
    """Define the arguments for the Graph Generator"""
    parser = ArgumentParser(description="Graph generator")
    parser.add_argument(
        "--num_nodes",
        type=int,
        required=True,
        help="Number of nodes in the graph. Can be a single integer or a list of integers to generate multiple graphs",
    )
    parser.add_argument(
        "--num_edges",
        type=int,
        required=True,
        help="Number of edges in the graph. Can be a single integer or a list of integers to generate multiple graphs",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Directory to save the generated graphs",
    )
    parser.add_argument(
        "--num_graphs",
        type=int,
        required=True,
        help="Number of graphs to generate",
    )
    parser.add_argument(
        "--generation_strategy",
        type=str,
        default="albert_barabasi",
        help="Graph generation strategy to use",
    )
    parser.add_argument(
        "--save_format",
        type=str,
        default=["data"],
        help="Format to save the generated graphs",
    )
    parser.add_argument(
        "--labels",
        type=str,
        default=None,
        help='Path to the labels JSON file. It must be of the form {"node_labels": ["lab1", ...], "edge_labels": ["labA", ...]}',
    )
    parser.add_argument(
        "--labels_strategy",
        type=str,
        default="random",
        help="Strategy to assign labels to nodes and edges",
    )
    args = parser.parse_args()
    return MainArgs(
        num_nodes=args.num_nodes,
        num_edges=args.num_edges,
        output_dir=args.output_dir,
        num_graphs=args.num_graphs,
        generation_strategy=args.generation_strategy,
        save_format=args.save_format,
        labels=args.labels,
        labels_strategy=args.labels_strategy,
    )
