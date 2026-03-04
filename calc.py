import math

def calculate_P_L(L):
    product = 1
    for j in range(1, L):
        for k in range(j + 1, L):
            term = 4 - 2 * math.cos(j * math.pi / L) - 2 * math.cos(k * math.pi / L)
            product *= term
    return round(product)

def main():
    print("L | P_L")
    print("---------")
    for L in range(3, 15):
        print(f"{L} | {calculate_P_L(L)}")

if __name__ == "__main__":
    main()