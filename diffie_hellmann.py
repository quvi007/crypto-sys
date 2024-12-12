import random

def bigMod(a, b, mod):
    if b == 0:
        return 1
    ans = bigMod(a, b >> 1, mod)
    ans = (ans * ans) % mod
    if b & 1:
        ans = (ans * (a % mod)) % mod
    return ans

def check_composite(n, a, d, s):
    x = bigMod(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for r in range(1, s):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True

def MillerRabin(n, iter = 5):
    if n < 4:
        return n == 2 or n == 3

    s = 0
    d = n - 1
    while d & 1 == 0:
        d >>= 1
        s += 1

    for i in range(iter):
        a = random.randint(2, n - 2)
        if check_composite(n, a, d, s):
            return False
    return True

def generatePrime(k):
    a = (1 << (k - 1))
    b = (1 << k) - 1
    while True:
        n = random.randint(a, b)
        if MillerRabin(n, 5):
            return n

def generateSafePrime(k):
    while (True):
        q = generatePrime(k - 1)
        p = 2 * q + 1
        if MillerRabin(p, 5):
            return p

def primitiveRoot(p, MIN, MAX):
    while True:
        g = random.randint(MIN, MAX)
        if bigMod(g, 2, p) != 1:
            if bigMod(g, (p - 1) >> 1, p) != 1:
                return g