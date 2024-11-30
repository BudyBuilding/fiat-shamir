import random
import hashlib
from math import gcd
from sympy import isprime, randprime

def hash_function(data):
    """Egyszerű hash függvény SHA-256-tal."""
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)

def fiat_shamir_proof(p, q, s):
    """
    Fiat-Shamir protokoll implementáció.
    
    Args:
        p (int): Egy nagy prímszám.
        q (int): Egy másik nagy prímszám.
        s (int): A titkos kulcs (gcd(s, n) = 1).
    
    Returns:
        None: Csak kimenetet generál.
    """
    n = p * q  # Publikus modulus
    v = pow(s, 2, n)  # Verifier kulcs (v = s^2 mod n)
    print(f"Publikus modulus (n): {n}")
    print(f"Verifier kulcs (v): {v} (számított: s^2 mod n)")

    # A bizonyító véletlenszerű értéket választ
    r = random.randint(1, n - 1)
    x = pow(r, 2, n)  # Publikus érték x = r^2 mod n
    print(f"\nBizonyító által választott véletlenszám (r): {r}")
    print(f"Publikusan megosztott érték (x): {x} (számított: r^2 mod n)")

    # A hash függvény felhasználása a kihívás generálásához
    c = hash_function(str(x)) % 2  # Kihívás értéke: c = hash(x) mod 2
    print(f"\nHash alapján generált kihívás (c): {c} (érték: hash(x) mod 2)")

    # A válasz kiszámítása
    y = (r * pow(s, c, n)) % n
    print(f"\nBizonyító válasza (y): {y} (számított: r * s^c mod n)")

    # Az ellenőrző oldali verifikáció
    x_prime = (pow(y, 2, n) * pow(v, c, n)) % n  # x' = y^2 * v^c mod n
    print(f"\nEllenőrző által számított érték (x'): {x_prime} (számított: y^2 * v^c mod n)")

    # Ellenőrzés, hogy az x' egyezik-e az eredeti x-szel
    if x == x_prime:
        print("\nA bizonyítás sikeres! Az x' megegyezik az eredeti x-szel.")
    else:
        print("\nA bizonyítás nem sikerült! Az x' nem egyezik meg az eredeti x-szel.")

# Példa használat
if __name__ == "__main__":
    # Véletlenszerű nagy prímszámok generálása
    p = randprime(2**(16-1), 2**16)  # 16 bites prímszám
    q = randprime(2**(16-1), 2**16)  # 16 bites prímszám

    # Titkos kulcs generálása (relatív prím n-hez)
    n = p * q
    while True:
        s = random.randint(2, n - 1)
        if gcd(s, n) == 1:
            break

    print(f"Generált értékek:\nPrím p: {p}\nPrím q: {q}\nTitkos kulcs (s): {s}")
    
    # Fiat-Shamir protokoll futtatása
    fiat_shamir_proof(p, q, s)
