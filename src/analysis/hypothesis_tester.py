"""
Hypothesis testing framework.

Provides tools to systematically test conjectures against collections of graphs.
"""

from typing import Callable
import networkx as nx
from src.invariants import compute_invariants
from src.graphs.generators import common_families


def test_hypothesis(
    predicate: Callable[[nx.Graph, dict], bool],
    graphs: list[nx.Graph] | None = None,
    invariants: list[str] | None = None,
    verbose: bool = True,
) -> dict:
    """
    Test a hypothesis (predicate) against a collection of graphs.

    Args:
        predicate: function (G, invariants_dict) -> bool
                   Returns True if hypothesis holds for G.
        graphs: list of graphs to test against (uses common families if None).
        invariants: which invariants to compute for each graph.
        verbose: print progress and results.

    Returns:
        dict with keys:
            - "passed": bool (True if all graphs satisfy the predicate)
            - "total": int (number of graphs tested)
            - "counterexamples": list of (graph, invariants) that fail
            - "results": list of (graph, invariants, holds) for all graphs
    """
    if graphs is None:
        graphs = []
        for family_graphs in common_families(8).values():
            graphs.extend(family_graphs)

    results = []
    counterexamples = []

    for i, G in enumerate(graphs):
        inv = compute_invariants(G, invariants)
        try:
            holds = predicate(G, inv)
        except Exception as e:
            holds = False
            inv["_error"] = str(e)

        results.append((G, inv, holds))
        if not holds:
            counterexamples.append((G, inv))
            if verbose:
                print(f"  COUNTEREXAMPLE #{len(counterexamples)}: "
                      f"n={inv.get('n', '?')}, m={inv.get('m', '?')} — {inv}")

    if verbose:
        status = "PASSED" if not counterexamples else "FAILED"
        print(f"\n[{status}] Tested {len(graphs)} graphs, "
              f"{len(counterexamples)} counterexample(s) found.")

    return {
        "passed": len(counterexamples) == 0,
        "total": len(graphs),
        "counterexamples": counterexamples,
        "results": results,
    }
