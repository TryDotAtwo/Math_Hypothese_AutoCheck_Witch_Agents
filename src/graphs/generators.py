"""
Standard graph generators for hypothesis testing.

Wraps networkx generators and adds batch generation utilities
for systematic hypothesis verification.
"""

from typing import Iterator
import networkx as nx
from itertools import combinations


def all_graphs(n: int) -> Iterator[nx.Graph]:
    """Yield all non-isomorphic graphs on n vertices (via nauty_geng if available)."""
    try:
        yield from nx.graph_atlas_g()[:] if n <= 7 else _generate_brute(n)
    except Exception:
        yield from _generate_brute(n)


def _generate_brute(n: int) -> Iterator[nx.Graph]:
    """Brute-force generation for small n — use nauty for anything serious."""
    vertices = list(range(n))
    possible_edges = list(combinations(vertices, 2))
    seen = []

    for r in range(len(possible_edges) + 1):
        for edges in combinations(possible_edges, r):
            G = nx.Graph()
            G.add_nodes_from(vertices)
            G.add_edges_from(edges)

            is_new = True
            for H in seen:
                if nx.is_isomorphic(G, H):
                    is_new = False
                    break
            if is_new:
                seen.append(G.copy())
                yield G


def random_graph(n: int, p: float = 0.5, seed: int | None = None) -> nx.Graph:
    """Erdos-Renyi random graph G(n, p)."""
    return nx.erdos_renyi_graph(n, p, seed=seed)


def common_families(max_n: int = 10) -> dict[str, list[nx.Graph]]:
    """Generate standard graph families for systematic testing."""
    families = {
        "complete": [nx.complete_graph(n) for n in range(2, max_n + 1)],
        "cycle": [nx.cycle_graph(n) for n in range(3, max_n + 1)],
        "path": [nx.path_graph(n) for n in range(2, max_n + 1)],
        "star": [nx.star_graph(n) for n in range(2, max_n + 1)],
        "petersen": [nx.petersen_graph()],
        "complete_bipartite": [
            nx.complete_bipartite_graph(a, b)
            for a in range(1, max_n // 2 + 1)
            for b in range(a, max_n - a + 1)
        ],
        "wheel": [nx.wheel_graph(n) for n in range(4, max_n + 1)],
        "grid": [
            nx.grid_2d_graph(a, b)
            for a in range(2, int(max_n**0.5) + 2)
            for b in range(a, int(max_n**0.5) + 2)
        ],
        "tree": [nx.random_tree(n, seed=42) for n in range(2, max_n + 1)],
    }
    return families
