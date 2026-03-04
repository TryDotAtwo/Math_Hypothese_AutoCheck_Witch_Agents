"""Smoke tests for invariant computations."""

import networkx as nx
from src.invariants import compute_invariants


def test_complete_graph_invariants():
    K5 = nx.complete_graph(5)
    inv = compute_invariants(K5, ["n", "m", "omega", "Delta", "delta"])
    assert inv["n"] == 5
    assert inv["m"] == 10
    assert inv["omega"] == 5
    assert inv["Delta"] == 4
    assert inv["delta"] == 4


def test_cycle_graph_invariants():
    C6 = nx.cycle_graph(6)
    inv = compute_invariants(C6, ["n", "m", "Delta", "delta", "girth"])
    assert inv["n"] == 6
    assert inv["m"] == 6
    assert inv["Delta"] == 2
    assert inv["delta"] == 2
    assert inv["girth"] == 6


def test_empty_graph():
    G = nx.Graph()
    inv = compute_invariants(G, ["n", "m"])
    assert inv["n"] == 0
    assert inv["m"] == 0


def test_petersen_graph():
    P = nx.petersen_graph()
    inv = compute_invariants(P, ["n", "m", "Delta", "delta", "girth", "diameter"])
    assert inv["n"] == 10
    assert inv["m"] == 15
    assert inv["Delta"] == 3
    assert inv["delta"] == 3
    assert inv["girth"] == 5
    assert inv["diameter"] == 2
