import numpy as np

def build_H(L, delta):
    # states are pairs (n, m) with 1 <= n < m <= L
    states = [(n, m) for n in range(1, L+1) for m in range(n+1, L+1)]
    dim = len(states)
    state_to_idx = {s: i for i, s in enumerate(states)}
    
    H = np.zeros((dim, dim))
    
    for i, (n, m) in enumerate(states):
        # Diagonal term:
        # For each bond (j, j+1), if it has 0 or 2 magnons, S^z_j S^z_{j+1} = 1/4
        # If it has 1 magnon, S^z_j S^z_{j+1} = -1/4
        # So 1/4 - S^z_j S^z_{j+1} is 0 for 0 or 2 magnons, and 1/2 for 1 magnon.
        # How many bonds have exactly 1 magnon?
        # A magnon at n contributes 1 to bonds (n-1, n) and (n, n+1), UNLESS n is on the boundary.
        # Boundary: n=1 -> bond (1,2). n=L -> bond (L-1, L).
        
        # Let's count exactly.
        # string of spins: + + - + + - + +
        # A bond (j, j+1) gives 1/2 if spins are anti-aligned.
        diag = 0
        for j in range(1, L):
            spin1 = -1 if j in (n, m) else 1
            spin2 = -1 if (j+1) in (n, m) else 1
            if spin1 != spin2:
                diag += 0.5 * delta # wait, if H = \sum (1/4 - S_z S_z)\Delta + ...
                # Actually, let's use the definition: H = \sum ( \Delta/4 - \Delta S_z S_z - 1/2 (S^+ S^- + S^- S^+) )
                # For \Delta=1, this is 1/4 - S_z S_z - 1/2(S^+S^-).
                # No, standard definition: 1/2 \sum (1 - \sigma^z \sigma^z \Delta - \dots)
                # Let's use: diagonal is \Delta * (number of anti-aligned bonds / 2)
                # Wait, C-001 says H = \sum (1/4 - S_j \cdot S_{j+1})
                # = \sum (1/4 - S^z_j S^z_{j+1} - 1/2 S^+_j S^-_{j+1} - 1/2 S^-_j S^+_{j+1})
                # If we put \Delta on the Z part:
                # 1/4 - \Delta S^z_j S^z_{j+1}.
                # But to make the energy of vacuum 0 for all \Delta, we need \Delta/4 - \Delta S^z S^z.
                pass
        
        # Let's just implement the matrix directly
        diag_val = 0
        for j in range(1, L):
            s1 = -1/2 if j in (n, m) else 1/2
            s2 = -1/2 if (j+1) in (n, m) else 1/2
            diag_val += (1/4 - s1 * s2) * delta
        H[i, i] = diag_val
        
        # Off-diagonal
        for j in range(1, L):
            # hopping between j and j+1
            # requires one spin to be up, one down
            s1 = j in (n, m)
            s2 = (j+1) in (n, m)
            if s1 != s2:
                # new state
                new_state = list((n, m))
                if s1:
                    new_state.remove(j)
                    new_state.append(j+1)
                else:
                    new_state.remove(j+1)
                    new_state.append(j)
                new_state.sort()
                new_state = tuple(new_state)
                H[i, state_to_idx[new_state]] = -0.5

    return H

for L in [3, 4, 5]:
    for delta in [0, 0.5, 1.0]:
        H = build_H(L, delta)
        det = np.linalg.det(H)
        print(f"L={L}, delta={delta}, det={det:.4f}")
