"""General-purpose helpers."""

import csv
from pathlib import Path
import networkx as nx
from src.invariants import compute_invariants


def graph_summary(G: nx.Graph, name: str = "") -> str:
    """One-line summary of a graph."""
    n = G.number_of_nodes()
    m = G.number_of_edges()
    conn = "connected" if nx.is_connected(G) else "disconnected"
    return f"{name + ': ' if name else ''}n={n}, m={m}, {conn}"


def export_invariants_csv(
    graphs: list[tuple[str, nx.Graph]],
    output_path: str | Path,
    invariants: list[str] | None = None,
) -> Path:
    """Compute invariants for a list of (name, graph) pairs and export to CSV."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_data = []
    for name, G in graphs:
        inv = compute_invariants(G, invariants)
        inv["name"] = name
        all_data.append(inv)

    if not all_data:
        return output_path

    fieldnames = ["name"] + [k for k in all_data[0] if k != "name"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)

    return output_path
