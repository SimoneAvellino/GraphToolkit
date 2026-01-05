import networkx as nx
from collections import deque
import numpy as np
import random


class DirectedGraph(nx.MultiDiGraph):

    def __init__(self, graph=None, **attr):
        super().__init__(graph, **attr)

    def extract_k_distant_nodes(self, k: int, num_landmarks: int = 20) -> list:
        """
        Ultra-fast distance approximation for large graphs using Landmark Sketching.

        Args:
            k: Number of distant nodes to extract.
            num_landmarks: Number of landmark nodes to use for distance approximation.
        """
        num_nodes = self.number_of_nodes()
        if k <= 0:
            return []
        if k >= num_nodes:
            return list(self.nodes())

        nodes = list(self.nodes())
        node_to_idx = {node: i for i, node in enumerate(nodes)}

        # 1. Select random landmarks
        # We use random sampling as it provides good coverage of the graph 'volume'
        landmarks = random.sample(nodes, min(num_landmarks, num_nodes))

        # 2. Build the Distance Matrix (O(L * (V+E)))
        # We use a 16-bit or 32-bit int to save memory at 500k scale
        # Value 'num_nodes' acts as a proxy for infinity (unreachable)
        G_undirected = self.to_undirected()
        dist_matrix = np.full((num_nodes, len(landmarks)), num_nodes, dtype=np.int32)

        for i, landmark in enumerate(landmarks):
            # Single-source BFS
            lengths = nx.single_source_shortest_path_length(G_undirected, landmark)
            for node, dist in lengths.items():
                dist_matrix[node_to_idx[node], i] = dist

        # 3. Greedy Vector Selection (O(k * N))
        # Start with the node furthest from the first landmark to avoid 'center' nodes
        first_idx = np.argmax(dist_matrix[:, 0])
        selected_indices = [first_idx]

        # Initialize min_dists with distances to the first selected node
        # Using Manhattan distance (L1 norm) on landmark vectors
        current_vec = dist_matrix[first_idx]
        min_dists = np.sum(np.abs(dist_matrix - current_vec), axis=1).astype(np.float64)

        for _ in range(k - 1):
            # Select node with largest minimum distance to the current set
            farthest_idx = np.argmax(min_dists)
            selected_indices.append(farthest_idx)

            # Update distances: compare existing min_dist vs distance to new node
            new_vec = dist_matrix[farthest_idx]
            dist_to_new = np.sum(np.abs(dist_matrix - new_vec), axis=1)

            # Vectorized update is extremely fast in NumPy
            min_dists = np.minimum(min_dists, dist_to_new)

        return [nodes[i] for i in selected_indices]

    def extract_subgraph_by_edge_count(self, source_node, num_edges) -> "DirectedGraph":
        """BFS expansion that collects up to ``num_edges`` edges, keeping attributes."""
        if source_node not in self:
            raise ValueError(f"Node {source_node} not found in graph.")

        subgraph = self.__class__()

        def add_node_with_attrs(node):
            if node not in subgraph:
                subgraph.add_node(node, **self.nodes[node])

        if num_edges <= 0:
            add_node_with_attrs(source_node)
            return subgraph

        queue = deque([source_node])
        visited_nodes = {source_node}
        visited_edges = set()
        edges_count = 0

        add_node_with_attrs(source_node)

        def edge_iter(node):
            # Treat the graph as undirected for traversal: explore both directions
            yield from self.out_edges(node, data=True, keys=True)
            yield from self.in_edges(node, data=True, keys=True)

        while queue and edges_count < num_edges:
            u = queue.popleft()

            for src, dst, key, data in edge_iter(u):
                edge_id = (src, dst, key)
                if edge_id in visited_edges:
                    continue

                visited_edges.add(edge_id)

                add_node_with_attrs(src)
                add_node_with_attrs(dst)
                subgraph.add_edge(src, dst, key=key, **data)
                edges_count += 1

                # Traverse outward in both directions to keep growing the frontier
                if dst not in visited_nodes:
                    visited_nodes.add(dst)
                    queue.append(dst)
                if src not in visited_nodes:
                    visited_nodes.add(src)
                    queue.append(src)

                if edges_count >= num_edges:
                    return subgraph

        return subgraph


class DBGraph(DirectedGraph):
    def __init__(self, graph=None, graph_id=None, **attr):
        super().__init__(graph, **attr)
        self._graph_id = graph_id

    def get_graph_id(self):
        return self._graph_id

    def set_graph_id(self, graph_id):
        self._graph_id = graph_id

    def copy(self):
        new_graph = DBGraph(graph_id=self._graph_id)
        new_graph.add_nodes_from(self.nodes(data=True))
        new_graph.add_edges_from(self.edges(data=True, keys=True))
        return new_graph
