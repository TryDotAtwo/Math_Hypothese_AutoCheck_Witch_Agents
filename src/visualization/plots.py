"""
Visualization utilities for graphs and invariant analysis.
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


FIGURES_DIR = Path(__file__).parent.parent.parent / "figures"


def draw_graph(
    G: nx.Graph,
    title: str = "",
    highlight_nodes: list | None = None,
    save_as: str | None = None,
    ax: plt.Axes | None = None,
) -> plt.Figure:
    """Draw a graph with optional node highlighting."""
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    else:
        fig = ax.figure

    pos = nx.spring_layout(G, seed=42)

    node_colors = ["#4A90D9"] * G.number_of_nodes()
    if highlight_nodes:
        node_list = list(G.nodes())
        for i, node in enumerate(node_list):
            if node in highlight_nodes:
                node_colors[i] = "#E74C3C"

    nx.draw(
        G, pos, ax=ax,
        with_labels=True,
        node_color=node_colors,
        node_size=500,
        edge_color="#888888",
        font_size=10,
        font_weight="bold",
        width=1.5,
    )
    if title:
        ax.set_title(title, fontsize=14)

    if save_as:
        path = FIGURES_DIR / save_as
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150, bbox_inches="tight")

    return fig


def plot_invariant_scatter(
    data: list[dict],
    x_key: str,
    y_key: str,
    title: str = "",
    save_as: str | None = None,
) -> plt.Figure:
    """Scatter plot of two invariants across a collection of graphs."""
    xs = [d[x_key] for d in data if x_key in d and y_key in d]
    ys = [d[y_key] for d in data if x_key in d and y_key in d]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(xs, ys, alpha=0.6, edgecolors="black", s=60)
    ax.set_xlabel(x_key, fontsize=12)
    ax.set_ylabel(y_key, fontsize=12)
    ax.set_title(title or f"{y_key} vs {x_key}", fontsize=14)
    ax.grid(True, alpha=0.3)

    if save_as:
        path = FIGURES_DIR / save_as
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150, bbox_inches="tight")

    return fig
