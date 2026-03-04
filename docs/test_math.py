import math
import json
import urllib.request

for L in range(3, 10):
    p = 1.0
    for j in range(1, L):
        for k in range(j+1, L):
            p *= (4 - 2*math.cos(j*math.pi/L) - 2*math.cos(k*math.pi/L))
    print(f'L={L}, P={round(p)}')

try:
    url = "https://oeis.org/search?q=A007726&fmt=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("OEIS A007726 data:")
        if data and isinstance(data, list) and len(data) > 0:
            print("Name:", data[0].get("name"))
            print("Data:", data[0].get("data"))
            print("Comments:", data[0].get("comment", [])[:3])
            print("Formulas:", data[0].get("formula", [])[:3])
            print("References:", data[0].get("reference", [])[:3])
except Exception as e:
    print(f"Failed to fetch OEIS: {e}")
