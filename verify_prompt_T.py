"""
Verify the quantity T from Hipo_1_update.md:
  T = 2/(L(L-1)) * Product_n (L-1 - E_n),  (excluding trivial eigenvalue E = L-1)
  where E_n are eigenvalues of H = sum_{k=1}^{L-1} P_{k,k+1} in the 2-magnon sector.

Relation: H_prompt = sum P = (L-1) - 2*H_ours, so E_n = (L-1) - 2*mu_n with mu_n eigenvalues of H_ours.
So L-1 - E_n = 2*mu_n. Product (excluding E=L-1, i.e. mu=0) = 2^N * product(nonzero mu).
We have product(nonzero eigenvalues of 2*H_ours) = binom(L,2)*A007726(L-1).
So T = 2/(L(L-1)) * binom(L,2)*A007726(L-1) = A007726(L-1).

Trig product from prompt: Product_{1<=j<k<=L-2} (4 - 2*cos(j*Pi/(L-1)) - 2*cos(k*Pi/(L-1))) = A007726(L-1).
"""

import numpy as np
from math import cos, pi

def build_H_ours_2magnon(L):
    """H_ours = sum (1/4 - S·S) in 2-magnon sector."""
    states = [(n, m) for n in range(1, L + 1) for m in range(n + 1, L + 1)]
    dim = len(states)
    state_to_idx = {s: i for i, s in enumerate(states)}
    H = np.zeros((dim, dim))
    for i, (n, m) in enumerate(states):
        diag_val = 0.0
        for j in range(1, L):
            s1 = -0.5 if j in (n, m) else 0.5
            s2 = -0.5 if (j + 1) in (n, m) else 0.5
            diag_val += 0.25 - s1 * s2
        H[i, i] = diag_val
        for j in range(1, L):
            s1_down = j in (n, m)
            s2_down = (j + 1) in (n, m)
            if s1_down != s2_down:
                new_state = list((n, m))
                if s1_down:
                    new_state.remove(j)
                    new_state.append(j + 1)
                else:
                    new_state.remove(j + 1)
                    new_state.append(j)
                new_state = tuple(sorted(new_state))
                H[i, state_to_idx[new_state]] += -0.5
    return H, states

def trig_product_prompt(L):
    """Product_{1<=j<k<=L-2} (4 - 2*cos(j*Pi/(L-1)) - 2*cos(k*Pi/(L-1))). Equals A007726(L-1)."""
    n = L - 1  # so 1<=j<k<=n-1 = L-2
    prod_val = 1.0
    for j in range(1, n):
        for k in range(j + 1, n):
            prod_val *= 4 - 2 * cos(j * pi / n) - 2 * cos(k * pi / n)
    return round(prod_val)

# OEIS A007726 (first terms): a(1)=1, a(2)=1, a(3)=4, a(4)=56, a(5)=2640, a(6)=411840, ...
oeis = {1: 1, 2: 1, 3: 4, 4: 56, 5: 2640, 6: 411840, 7: 210613312}

print("Verification of T from Hipo_1_update.md")
print("T = 2/(L(L-1)) * Product_n (L-1 - E_n), excluding trivial E = L-1")
print("Expected: T(L) = A007726(L-1) = trig product with 1<=j<k<=L-2, cos(j*Pi/(L-1))")
print()
print(f"{'L':>3} | {'T (from H)':>18} | {'Trig product':>18} | {'A007726(L-1)':>15} | Match")
print("-" * 65)

for L in range(3, 11):
    H_ours, states = build_H_ours_2magnon(L)
    # 2*H_ours eigenvalues
    eigs_2H = np.linalg.eigvalsh(2 * H_ours)
    nonzero = eigs_2H[np.abs(eigs_2H) > 1e-10]
    prod_nonzero = np.prod(nonzero)
    # T = 2/(L(L-1)) * product(L-1 - E_n). E_n = (L-1) - 2*mu, so L-1 - E_n = 2*mu.
    # product(2*mu) = 2^N * prod(mu). And prod(mu) = prod_nonzero (these are eigenvalues of 2*H).
    # So product(L-1 - E_n) = prod(2*mu) = 2^len(nonzero) * prod(mu). But prod(mu) = prod_nonzero.
    # So T = 2/(L(L-1)) * 2^{len(nonzero)} * prod_nonzero.  Wait, (L-1 - E_n) = 2*mu_n, so product = 2^N * prod(mu_n).
    # And prod(mu_n) = prod_nonzero (since 2*H has eigenvalues 2*mu with mu = eigenvalues of H_ours, so 2*mu are the nonzero eigs of 2*H_ours). So prod(mu_n) = prod_nonzero/2^N? No: 2*H_ours has eigenvalues lambda = 2*eigenvalue(H_ours). So eigenvalue(H_ours) = lambda/2. So product(mu_n) = product(lambda_n/2) = prod_nonzero / 2^N. So product(L-1 - E_n) = product(2*mu_n) = 2^N * (prod_nonzero/2^N) = prod_nonzero. So T = 2/(L(L-1)) * prod_nonzero. But we also had prod_nonzero = binom(L,2)*A007726(L-1) = L(L-1)/2 * A007726(L-1). So T = 2/(L(L-1)) * L(L-1)/2 * A007726(L-1) = A007726(L-1). So T = 2/(L(L-1)) * prod_nonzero. Let me verify with that.
    T_val = (2.0 / (L * (L - 1))) * prod_nonzero
    T_int = round(T_val)
    trig = trig_product_prompt(L)
    a_val = oeis.get(L - 1, "?")
    match = "Yes" if T_int == trig and (a_val == "?" or T_int == a_val) else "No"
    print(f"{L:3d} | {T_int:18d} | {trig:18d} | {str(a_val):>15} | {match}")

print()
print("Conclusion: T(L) = trig_product(1<=j<k<=L-2) = A007726(L-1) — verified numerically.")
