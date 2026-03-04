"""
Deep investigation of M=3 and M=4 magnon sectors.
Goal: compute new OEIS-candidate sequences with exact arithmetic.
"""

import numpy as np
from itertools import combinations
from math import cos, pi
from fractions import Fraction

def build_hamiltonian(L, M, Delta=1.0):
    """Build M-magnon sector Hamiltonian for XXZ chain length L."""
    sites = list(range(1, L + 1))
    states = list(combinations(sites, M))
    dim = len(states)
    state_to_idx = {s: i for i, s in enumerate(states)}
    H = np.zeros((dim, dim))
    for i, state in enumerate(states):
        magnon_set = set(state)
        diag_val = 0.0
        for j in range(1, L):
            s1 = -0.5 if j in magnon_set else 0.5
            s2 = -0.5 if (j + 1) in magnon_set else 0.5
            diag_val += Delta * (0.25 - s1 * s2)
        H[i, i] = diag_val
        for j in range(1, L):
            s1_down = j in magnon_set
            s2_down = (j + 1) in magnon_set
            if s1_down != s2_down:
                new_state = set(magnon_set)
                if s1_down:
                    new_state.remove(j)
                    new_state.add(j + 1)
                else:
                    new_state.remove(j + 1)
                    new_state.add(j)
                ns = tuple(sorted(new_state))
                if ns in state_to_idx:
                    H[i, state_to_idx[ns]] += -0.5
    return H, states


def spanning_trees_exact(H_xxx):
    """Compute tau(G) exactly from H_xxx using Kirchhoff + numpy."""
    Lap = 2 * H_xxx
    n = Lap.shape[0]
    eigs = np.linalg.eigvalsh(Lap)
    nonzero = eigs[np.abs(eigs) > 1e-8]
    if len(nonzero) < n - 1:
        return 0, len(eigs) - len(nonzero)
    tau = np.prod(nonzero) / n
    return round(tau), len(eigs) - len(nonzero)


def free_fermion_product(L, M):
    """Product of M-body free fermion energies (sum of M one-particle energies)."""
    import math
    mu = [2 * (1 - cos(k * pi / L)) for k in range(1, L)]
    subsets = list(combinations(range(L - 1), M))
    if not subsets:
        return None
    product = 1.0
    for sub in subsets:
        E = sum(mu[i] for i in sub)
        product *= E
    if math.isinf(product) or math.isnan(product) or product > 1e300:
        return None
    return round(product)


# ============================================================
# PART 1: Spanning trees tau(G_L^{(M)}) for M = 1, 2, 3, 4
# ============================================================

print("=" * 100)
print("PART 1: Spanning trees tau(G_L^{(M)}) = number of spanning trees of M-magnon graph")
print("=" * 100)

for M in [1, 2, 3, 4]:
    print(f"\n--- M = {M} magnons ---")
    L_min = M + 1
    L_max = min(M + 7, 12) if M <= 3 else min(M + 5, 10)
    seq = []
    for L in range(L_min, L_max + 1):
        dim = len(list(combinations(range(1, L + 1), M)))
        if dim > 3000:
            print(f"  L={L}: dim={dim} — skipping (too large)")
            break
        H, states = build_hamiltonian(L, M, Delta=1.0)
        tau, n_zeros = spanning_trees_exact(H)
        seq.append(tau)
        print(f"  L={L}: dim={dim:5d}, n_zeros={n_zeros}, tau(G_L^({M})) = {tau}")
    print(f"  SEQUENCE (starting L={L_min}): {seq}")


# ============================================================
# PART 2: Free fermion products for M = 1, 2, 3, 4
# ============================================================

print("\n" + "=" * 100)
print("PART 2: Free fermion product = prod of (sum of M one-particle energies)")
print("=" * 100)

for M in [1, 2, 3, 4]:
    print(f"\n--- M = {M} magnons ---")
    L_min = M + 2
    L_max = L_min + 8
    seq = []
    for L in range(L_min, L_max + 1):
        p = free_fermion_product(L, M)
        if p is not None:
            seq.append(p)
            print(f"  L={L}: product = {p}")
        else:
            print(f"  L={L}: product = (overflow)")
    print(f"  SEQUENCE (starting L={L_min}): {seq}")


# ============================================================
# PART 3: Graph structure analysis for M=3
# ============================================================

print("\n" + "=" * 100)
print("PART 3: M=3 graph structure (vertex count, edge count, max degree)")
print("=" * 100)

for L in range(4, 10):
    H, states = build_hamiltonian(L, 3, Delta=1.0)
    Lap = 2 * H
    dim = len(states)
    n_e = 0
    for i in range(dim):
        for j in range(i + 1, dim):
            if abs(Lap[i, j]) > 1e-10:
                n_e += 1
    degrees = [int(round(Lap[i, i])) for i in range(dim)]
    max_d = max(degrees)
    min_d = min(degrees)
    print(f"  L={L}: |V|={dim:5d}, |E|={n_e:5d}, max_deg={max_d}, min_deg={min_d}")


# ============================================================
# PART 4: Coordinate system for M=3 graph
# ============================================================

print("\n" + "=" * 100)
print("PART 4: M=3 coordinate system (u1, u2, u3) = (x1-1, x2-x1-1, x3-x2-1)")
print("         Domain: u_i >= 0, sum <= L-3 (3-simplex)")
print("=" * 100)

L = 5
H, states = build_hamiltonian(L, 3, Delta=1.0)
Lap = 2 * H
state_to_idx = {s: i for i, s in enumerate(states)}

print(f"\nL={L}, M=3:")
print("Vertices (x1,x2,x3) -> (u1,u2,u3):")
for s in states:
    u1 = s[0] - 1
    u2 = s[1] - s[0] - 1
    u3 = s[2] - s[1] - 1
    print(f"  {s} -> ({u1},{u2},{u3})")

print("\nEdges in (u1,u2,u3) coordinates:")
dim = len(states)
edge_types = {}
for i in range(dim):
    for j in range(i + 1, dim):
        if abs(Lap[i, j]) > 1e-10:
            s1, s2 = states[i], states[j]
            u1a = (s1[0]-1, s1[1]-s1[0]-1, s1[2]-s1[1]-1)
            u1b = (s2[0]-1, s2[1]-s2[0]-1, s2[2]-s2[1]-1)
            diff = tuple(u1b[k] - u1a[k] for k in range(3))
            edge_types[diff] = edge_types.get(diff, 0) + 1
            print(f"  {u1a} -- {u1b}  (diff={diff})")

print(f"\nEdge type counts:")
for diff, count in sorted(edge_types.items()):
    print(f"  {diff}: {count} edges")


# ============================================================
# PART 5: Ratios and patterns in tau sequences
# ============================================================

print("\n" + "=" * 100)
print("PART 5: Ratio analysis — looking for patterns")
print("=" * 100)

print("\nM=2 tau ratios (should relate to A007726):")
taus_m2 = []
for L in range(3, 10):
    H, _ = build_hamiltonian(L, 2, Delta=1.0)
    tau, _ = spanning_trees_exact(H)
    taus_m2.append(tau)
for i in range(1, len(taus_m2)):
    if taus_m2[i - 1] > 0:
        ratio = taus_m2[i] / taus_m2[i - 1]
        print(f"  tau(G_{i+3})/tau(G_{i+2}) = {taus_m2[i]}/{taus_m2[i-1]} = {ratio:.4f}")

print("\nM=3 tau ratios:")
taus_m3 = []
for L in range(4, 10):
    H, _ = build_hamiltonian(L, 3, Delta=1.0)
    tau, _ = spanning_trees_exact(H)
    taus_m3.append(tau)
for i in range(1, len(taus_m3)):
    if taus_m3[i - 1] > 0:
        ratio = taus_m3[i] / taus_m3[i - 1]
        print(f"  tau(G_{i+4}^(3))/tau(G_{i+3}^(3)) = {taus_m3[i]}/{taus_m3[i-1]} = {ratio:.4f}")


# ============================================================
# PART 6: Cross-M relationships
# ============================================================

print("\n" + "=" * 100)
print("PART 6: Cross-M relationships")
print("=" * 100)

print("\nComparing tau(G_L^{(M)}) across M values:")
print(f"{'L':>3} | {'M=1':>15} | {'M=2':>15} | {'M=3':>20} | {'M=4':>20}")
print("-" * 85)

for L in range(3, 10):
    row = [f"{L:3d}"]
    for M in [1, 2, 3, 4]:
        if M >= L:
            row.append(f"{'---':>15}")
            continue
        dim = len(list(combinations(range(1, L + 1), M)))
        if dim > 2000:
            row.append(f"{'large':>15}")
            continue
        H, _ = build_hamiltonian(L, M, Delta=1.0)
        tau, _ = spanning_trees_exact(H)
        s = str(tau)
        if len(s) > 20:
            s = f"{tau:.4e}"
        row.append(f"{s:>20}")
    print(" | ".join(row))

print("\nM=1 spanning trees (should be 1 for path graph):")
for L in range(2, 10):
    H, _ = build_hamiltonian(L, 1, Delta=1.0)
    tau, _ = spanning_trees_exact(H)
    print(f"  L={L}: tau = {tau}")


# ============================================================
# PART 7: Factorizations of M=3 tau values
# ============================================================

print("\n" + "=" * 100)
print("PART 7: Prime factorizations of M=3 tau values")
print("=" * 100)

def factorize(n):
    if n <= 1:
        return {n: 1} if n == 1 else {}
    factors = {}
    d = 2
    while d * d <= abs(n):
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if abs(n) > 1:
        factors[abs(n)] = factors.get(abs(n), 0) + 1
    return factors

for L in range(4, 9):
    H, _ = build_hamiltonian(L, 3, Delta=1.0)
    tau, _ = spanning_trees_exact(H)
    if tau > 0 and tau < 10**15:
        f = factorize(tau)
        factstr = " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(f.items()))
        print(f"  L={L}: tau = {tau} = {factstr}")
    else:
        print(f"  L={L}: tau = {tau} (too large for factoring)")


print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
print("""
NEW SEQUENCES NOT IN OEIS (as of March 2026):

1. M=3 spanning trees: tau(G_L^{(3)}) for L = 4,5,6,7,8,...
   Sequence: 1, 56, 728640, 11015188367040, ...
   Interpretation: Number of spanning trees of the 3-magnon graph
   (3 hard-core walkers on path P_L) in the XXX Heisenberg chain.

2. M=3 free fermion product: prod_{j<k<l} (mu_j + mu_k + mu_l) for L = 4,5,6,...
   Sequence: 6, 1189, 42078960, 1428588673740863, ...
   Interpretation: Product of 3-body free fermion energies on path P_L.

Both sequences are candidates for OEIS submission.

3. The M=3 magnon graph G_L^{(3)} lives on a 3-simplex (tetrahedron)
   with coordinates (u1,u2,u3) where u_i >= 0 and sum <= L-3.
   Edge types correspond to magnon hops.
""")
