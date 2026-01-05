import typer
from typing import Optional

from alter import AlterOptions
from db import DBGraphs, DBGraph
from distributions.strategy import distribution_factory
from generator.labels.types import LABEL_STRATEGIES
from reader import InputFormat
from reify.strategy import reify_strategy_factory
from reify.types import ReifyStrategyTypes
from saver import OutputFormat, saver_factory
from generator.graphs.types import GRAPH_STRATEGIES

app = typer.Typer(help="Tool for graph manipulation and generation")


@app.command("convert")
def convert(
    input_path: str = typer.Argument(..., help="Path to the source file"),
    input_format: InputFormat = typer.Argument(..., help="Source format"),
    output_path: Optional[str] = typer.Argument(None, help="Path to the output file"),
    output_format: OutputFormat = typer.Argument(..., help="Destination format"),
):
    """
    Reads a graph and converts it to a different format.
    """
    from reader import reader_factory

    reader = reader_factory(input_format)
    saver = saver_factory(output_format)

    if output_path is None:
        output_path = f"output.{output_format}"

    g = reader.read(input_path)
    saver.save(g, output_path)


@app.command("generate")
def generator(
    num_nodes: int = typer.Argument(..., help="Number of nodes"),
    num_edges: int = typer.Argument(..., help="Number of edges"),
    graph_strategy: GRAPH_STRATEGIES = typer.Argument(
        ..., help="Graph generation strategy"
    ),
    label_strategy: LABEL_STRATEGIES = typer.Argument(
        ..., help="Label assignment strategy"
    ),
    output_path: Optional[str] = typer.Argument(None, help="Path to the output file"),
    output_format: OutputFormat = typer.Argument(..., help="Destination format"),
):
    """
    Generates random graphs. The user can choose algorithms to
    generate the graph and optionally assign labels to nodes and edges.
    """
    from generator import generator_factory, label_factory

    graph_generator = generator_factory(graph_strategy, num_nodes, num_edges)
    label_generator = label_factory(label_strategy)
    saver = saver_factory(output_format)

    typer.echo("Generating graph...")
    g = graph_generator.generate()
    typer.echo("Assigning labels...")
    label_generator.assign(g)

    saver.save(g, output_path)


@app.command("db_construct")
def db_construct(
    graph_path: str = typer.Argument(
        ..., help="Path to the graph file to extract graphs from"
    ),
    input_format: InputFormat = typer.Argument(..., help="Source format"),
    db_size: int = typer.Argument(
        ..., help="Number of graphs to store in the database"
    ),
    edge_distribution: str = typer.Argument(
        ..., help="Distribution strategy for edge selection"
    ),
    output_path: str = typer.Argument(..., help="Path to the database to construct"),
    output_format: OutputFormat = typer.Argument(..., help="Database format"),
):
    """
    Constructs the database for storing graphs.
    """
    from reader import reader_factory
    from distributions import distribution_factory

    from saver import saver_factory

    reader = reader_factory(input_format)
    dist_strategy = distribution_factory(edge_distribution)
    saver = saver_factory(output_format)

    print("Reading main graph...", end="", flush=True)
    g = reader.read(graph_path)
    print(f" done. {g}", flush=True)

    max_edges = g.number_of_edges()

    print("Constructing database:")
    print(f" - Find {db_size} starting nodes...", end="", flush=True)
    starting_nodes = g.extract_k_distant_nodes(db_size)
    print(" done.")

    for i, node in enumerate(starting_nodes):

        num_edges = int(dist_strategy.get())
        if num_edges > max_edges:
            print(
                f"     - Warning: requested {num_edges} edges, but max is {max_edges}. Using {max_edges} instead."
            )
            num_edges = max_edges
        print(
            f"   - Extracting subgraph {i+1}/{db_size} with {num_edges} edges...",
            end="",
            flush=True,
        )
        subgraph = g.extract_subgraph_by_edge_count(node, num_edges)
        print(f" done. {subgraph}")
        # Wrap extracted graph with an id so saver can serialize it
        db_graph = DBGraph(subgraph, graph_id=i)
        db_batch = DBGraphs([db_graph])
        print("    - Saving to database...", end="", flush=True)
        saver.save_db(db_batch, output_path, append=True)
        print(" done.")
        # Free memory
        del subgraph


@app.command("reify_db")
def reify_graph(
    input_path: str = typer.Argument(..., help="Path to the source file"),
    input_format: InputFormat = typer.Argument(..., help="Source format"),
    output_path: str = typer.Argument(..., help="Path to the output file"),
    output_format: OutputFormat = typer.Argument(..., help="Destination format"),
    strategy: ReifyStrategyTypes = typer.Argument(..., help="Reification strategy"),
):
    """
    Reifies a database of graphs using the Multi-Arcs Expansion strategy.
    """
    from reader import reader_factory
    from saver import saver_factory
    from reify import Reificator, reify_strategy_factory

    reader = reader_factory(input_format)
    saver = saver_factory(output_format)
    db = reader.read_db(input_path)

    reif = Reificator(strategy=reify_strategy_factory(strategy))

    reif_db = DBGraphs()
    for g in db.get_graphs():
        print(f"Reifing graph {g.get_graph_id()}")
        reif_g = reif.reify(g)
        reif_db.add_graph(reif_g)

    print("Saving reified database...", end="")
    saver.save_db(reif_db, output_path)
    print("Done.")


@app.command("alter_db")
def alter_graph(
    input_path: str = typer.Argument(..., help="Path to the source file"),
    input_format: InputFormat = typer.Argument(..., help="Source format"),
    output_path: str = typer.Argument(..., help="Path to the output file"),
    output_format: OutputFormat = typer.Argument(..., help="Destination format"),
    strategy: AlterOptions = typer.Argument(..., help="Alteration strategy"),
):
    """
    Alters a graph in various ways (not yet implemented).
    """
    from reader import reader_factory
    from saver import saver_factory
    from alter import GraphAlter
    from alter.strategy import alter_strategy_factory

    reader = reader_factory(input_format)
    saver = saver_factory(output_format)
    alterer = GraphAlter(strategy=alter_strategy_factory(strategy))
    db = reader.read_db(input_path)
    multiedge_db = DBGraphs()
    for g in db.get_graphs():
        print(f"Altering graph {g.get_graph_id()}")
        altered_g = alterer.alter(g)
        print(alterer.what_changed(g, altered_g))
        multiedge_db.add_graph(altered_g)

    print("Saving altered database...", end="")
    saver.save_db(multiedge_db, output_path)
    print("Done.")


@app.command("sub_database")
def sub_database(
    input_path: str = typer.Argument(..., help="Path to the source file"),
    input_format: InputFormat = typer.Argument(..., help="Source format"),
    edge_distribution: str = typer.Argument(
        ..., help="Distribution strategy for edge selection"
    ),
    db_size: int = typer.Argument(
        ..., help="Number of graphs to include in the sub-database"
    ),
    output_path: str = typer.Argument(..., help="Path to the output file"),
    output_format: OutputFormat = typer.Argument(..., help="Destination format"),
):
    """
    Creates a sub-database containing for each graph in the original database a subgraph with a given distribution of edges.
    """
    from reader import reader_factory
    from saver import saver_factory
    from db import DBGraphs

    reader = reader_factory(input_format)
    saver = saver_factory(output_format)
    db = reader.read_db(input_path)

    if db_size > len(db.get_graphs()):
        raise ValueError(
            f"Requested sub-database size {db_size} exceeds original database size {len(db.get_graphs())}."
        )

    dist_strategy = distribution_factory(edge_distribution)

    sub_db = DBGraphs()

    graphs_to_process = db.get_graphs()[:db_size]

    for g in graphs_to_process:
        num_edges = int(dist_strategy.get())
        max_edges = g.number_of_edges()
        if num_edges > max_edges:
            print(
                f"     - Warning: requested {num_edges} edges, but max is {max_edges}. Using {max_edges} instead."
            )
            num_edges = max_edges
        print(
            f"   - Extracting subgraph of graph {g.get_graph_id()} with {num_edges} edges...",
            end="",
            flush=True,
        )
        start_node_id = list(g.nodes())[0]
        subgraph = g.extract_subgraph_by_edge_count(start_node_id, num_edges)
        print(f" done. {subgraph}")
        # Wrap extracted graph with an id so saver can serialize it
        sub_db.add_graph(DBGraph(subgraph, g.get_graph_id()))

    print("Saving sub-database...", end="")
    saver.save_db(sub_db, output_path)
    print("Done.")


if __name__ == "__main__":
    app()
