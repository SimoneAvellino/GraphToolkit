"""
This file contains a function that read a datagraph and converts it to a multigraph.

It add random arcs between existing nodes to create multiple edges.

The labels of the new edges are generated randomly and are choosen from the existing labels in the graph.
"""

from db import DBGraphs
from graph import DirectedGraph
from reader import reader_factory

from saver import saver_factory
import random


def to_multigraph(g: DirectedGraph):
    """
    Reads a datagraph from input_path, adds extra_edges random edges to create a multigraph,
    and saves the resulting multigraph to output_path. The labels of the new edges are generated
    based on the specified label_strategy.
    """
    # cicle through existing edges
    edges = list(g.edges(data=True))  # copy to avoid modification during iteration
    for u, v, data in edges:
        # flip a coin to decide whether to add extra edges between u and v
        rand = random.random()
        if rand < 0.8:
            continue

        # add extra edge between u and v with the same label of the existing edge
        g.add_edge(u, v, label=data["label"] + f"_extra")

    return g


if __name__ == "__main__":

    reader = reader_factory("data")
    saver = saver_factory("data")

    input_path = "/Users/simoneavellino/Desktop/grafi_cminer/prova.data"
    output_path = "/Users/simoneavellino/Desktop/grafi_cminer/m_prova.data"
    db = reader.read_db(input_path)

    multiedge_db = DBGraphs()

    for g in db.get_graphs():
        print(f"Processing graph {g.get_graph_id()}")
        prev_edge_count = g.number_of_edges()
        multigraph = to_multigraph(g)
        print(
            f"Graph {g.get_graph_id()} now has {multigraph.number_of_edges()} edges. (was {prev_edge_count}, added {multigraph.number_of_edges() - prev_edge_count} extra edges)"
        )
        multiedge_db.add_graph(multigraph)

    print("Saving multigraph database...", end="")
    saver.save_db(multiedge_db, output_path)
    print("Done.")
