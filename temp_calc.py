import math

def P(L):
    prod = 1.0
    for j in range(1, L):
        for k in range(j + 1, L):
            val = 4 - 2 * math.cos(j * math.pi / L) - 2 * math.cos(k * math.pi / L)
            prod *= val
    return round(prod)

print("P_L:")
for L in range(3, 10):
    print(f"L={L}: {P(L)}")
