<!-- @format -->

# Graph Generator CLI

A small toolkit for generating, converting, and manipulating graphs and graph databases. It wraps a set of pluggable strategies (graph generation, labeling, distributions, reification, alteration) behind a Typer-powered CLI.

## Installation

```bash
git clone https://github.com/SimoneAvellino/GraphToolkit
cd graph_generator
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Usage

Run any command with `--help` to see options:

```bash
python main.py --help # show the list of commands
python main.py [command] --help # show parameters for [command] and a brief description
```

## Commands

### convert

Read a graph in one format and save it in another.

```bash
python main.py convert <input_path> <input_format> [output_path] <output_format>
```

### generate

Generate a random graph, optionally label nodes/edges, and save it.

```bash
python main.py generate <num_nodes> <num_edges> <graph_strategy> <label_strategy> [output_path] <output_format>
```

### db_construct

Extract subgraphs from a source graph to build a database.

```bash
python main.py db_construct <graph_path> <input_format> <db_size> <edge_distribution> <output_path> <output_format>
```

### reify_db

Reify a database of graphs using a chosen strategy.

```bash
python main.py reify_db <input_path> <input_format> <output_path> <output_format> <strategy>
```

### alter_db

Alter graphs in a database using an alteration strategy.

```bash
python main.py alter_db <input_path> <input_format> <output_path> <output_format> <strategy>
```

### sub_database

Create a sub-database by extracting subgraphs with a specified edge distribution.

```bash
python main.py sub_database <input_path> <input_format> <edge_distribution> <db_size> <output_path> <output_format>
```

## Development

-   Explore strategies under `generator/graphs`, `generator/labels`, `distributions`, `reify`, `alter` to add or change behaviors.
-   Run formatting/linting as preferred; the project is pure Python.

## Troubleshooting

-   If enums/strategies are unclear, inspect the `strategy` and `types` modules in each subpackage and use `--help`.
-   For missing dependencies, reinstall the virtualenv and check `requirements.txt` if present.
