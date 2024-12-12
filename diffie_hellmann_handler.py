from diffie_hellmann import *
import time

def main():
    for k in [128, 192, 256]:
        print(f"k = {k}:")
        tp = tg = ta = tb = tA = tB = ts1 = ts2 = 0 
        trials = 5
        for i in range(trials):
            print(f"Trial {i}:")

            start_time = time.time()
            p = generateSafePrime(k)
            end_time = time.time()
            tp += end_time - start_time
            print(f"p = {p}")
            
            start_time = time.time()
            g = primitiveRoot(p, 2, p - 1)
            end_time = time.time()
            tg += end_time - start_time
            print(f"g = {g}")

            start_time = time.time()
            a = generatePrime(k >> 1)
            end_time = time.time()
            ta += end_time - start_time
            print(f"a = {a}")

            start_time = time.time()
            b = generatePrime(k >> 1)
            end_time = time.time()
            tb += end_time - start_time
            print(f"b = {b}")

            start_time = time.time()
            A = bigMod(g, a, p)
            end_time = time.time()
            tA += end_time - start_time
            print(f"A = {A}")
            
            start_time = time.time()
            B = bigMod(g, b, p)
            end_time = time.time()
            tB += end_time - start_time
            print(f"B = {B}")

            start_time = time.time()
            s1 = bigMod(A, b, p)
            end_time = time.time()
            ts1 += end_time - start_time
            print(f"s1 = {s1}")

            start_time = time.time()
            s2 = bigMod(B, a, p)
            end_time = time.time()
            ts2 += end_time - start_time
            print(f"s2 = {s2}")

            print(f"s1 == s2: {s1 == s2}")
            print()

        tp /= trials
        tg /= trials
        ta /= trials
        tb /= trials
        tA /= trials
        tB /= trials
        ts1 /= trials
        ts2 /= trials
        print()
        print(f"Average tp = {tp} seconds")
        print(f"Average tg = {tg} seconds")
        print(f"Average ta or tb = {(ta + tb) / 2} seconds")
        print(f"Average tA or tB = {(tA + tB) / 2} seconds")
        print(f"Average ts1 or ts2 = {(ts1 + ts2) / 2} seconds")
        print()

main()