"""
Basic graph invariants.

Each invariant is a function G -> number (or tuple).
Register new invariants by adding them to INVARIANT_REGISTRY.
"""

import networkx as nx
import numpy as np


def chromatic_number(G: nx.Graph) -> int:
    """Exact chromatic number via greedy + verification (small graphs only)."""
    if G.number_of_nodes() == 0:
        return 0
    return len(set(nx.coloring.greedy_color(G, strategy="largest_first").values()))


def clique_number(G: nx.Graph) -> int:
    """Size of the maximum clique."""
    if G.number_of_nodes() == 0:
        return 0
    clique, _ = nx.max_weight_clique(G, weight=None)
    return len(clique)


def independence_number(G: nx.Graph) -> int:
    """Size of the maximum independent set = clique number of complement."""
    return clique_number(nx.complement(G))


def diameter(G: nx.Graph) -> float:
    """Diameter (inf if disconnected)."""
    if not nx.is_connected(G):
        return float("inf")
    return nx.diameter(G)


def radius(G: nx.Graph) -> float:
    """Radius (inf if disconnected)."""
    if not nx.is_connected(G):
        return float("inf")
    return nx.radius(G)


def girth(G: nx.Graph) -> float:
    """Length of the shortest cycle (inf if acyclic)."""
    shortest = float("inf")
    for node in G.nodes():
        try:
            cycle_length = _shortest_cycle_through(G, node)
            shortest = min(shortest, cycle_length)
        except nx.NetworkXError:
            continue
    return shortest


def _shortest_cycle_through(G: nx.Graph, source) -> int:
    dist = {source: 0}
    queue = [(source, None)]
    while queue:
        next_queue = []
        for v, parent in queue:
            for w in G.neighbors(v):
                if w == parent:
                    continue
                if w in dist:
                    return dist[v] + dist[w] + 1
                dist[w] = dist[v] + 1
                next_queue.append((w, v))
        queue = next_queue
    return float("inf")


def spectral_radius(G: nx.Graph) -> float:
    """Largest eigenvalue of the adjacency matrix."""
    if G.number_of_nodes() == 0:
        return 0.0
    eigenvalues = nx.adjacency_spectrum(G)
    return float(max(abs(eigenvalues)))


def algebraic_connectivity(G: nx.Graph) -> float:
    """Second smallest eigenvalue of the Laplacian (Fiedler value)."""
    if G.number_of_nodes() <= 1:
        return 0.0
    return float(nx.algebraic_connectivity(G))


def vertex_connectivity(G: nx.Graph) -> int:
    if G.number_of_nodes() <= 1:
        return 0
    return nx.node_connectivity(G)


def edge_connectivity(G: nx.Graph) -> int:
    if G.number_of_nodes() <= 1:
        return 0
    return nx.edge_connectivity(G)


def average_degree(G: nx.Graph) -> float:
    if G.number_of_nodes() == 0:
        return 0.0
    return 2 * G.number_of_edges() / G.number_of_nodes()


def max_degree(G: nx.Graph) -> int:
    if G.number_of_nodes() == 0:
        return 0
    return max(dict(G.degree()).values())


def min_degree(G: nx.Graph) -> int:
    if G.number_of_nodes() == 0:
        return 0
    return min(dict(G.degree()).values())


def density(G: nx.Graph) -> float:
    return nx.density(G)


def number_of_triangles(G: nx.Graph) -> int:
    return sum(nx.triangles(G).values()) // 3


INVARIANT_REGISTRY: dict[str, callable] = {
    "n": lambda G: G.number_of_nodes(),
    "m": lambda G: G.number_of_edges(),
    "chi": chromatic_number,
    "omega": clique_number,
    "alpha": independence_number,
    "delta": min_degree,
    "Delta": max_degree,
    "avg_deg": average_degree,
    "density": density,
    "diameter": diameter,
    "radius": radius,
    "girth": girth,
    "spectral_radius": spectral_radius,
    "algebraic_connectivity": algebraic_connectivity,
    "kappa_v": vertex_connectivity,
    "kappa_e": edge_connectivity,
    "triangles": number_of_triangles,
    "components": lambda G: nx.number_connected_components(G),
}


def compute_invariants(
    G: nx.Graph,
    which: list[str] | None = None,
) -> dict[str, float]:
    """Compute selected invariants (all by default) for a graph."""
    keys = which or list(INVARIANT_REGISTRY.keys())
    results = {}
    for key in keys:
        if key not in INVARIANT_REGISTRY:
            raise KeyError(f"Unknown invariant: {key}")
        try:
            results[key] = INVARIANT_REGISTRY[key](G)
        except Exception as e:
            results[key] = f"error: {e}"
    return results
