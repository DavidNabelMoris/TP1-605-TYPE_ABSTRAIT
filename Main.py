import random

# ─── Assertions axiomatiques ───────────────────────────────────────────────────

def assert_check(condition, message):
    if not condition:
        raise AssertionError(f"[VIOLATION] {message}")



def precondition_partition(t, p, q):
    return 0 <= p <= q < len(t)


# ─── Procédure PARTITION alternative ──────────────────────────────────────────

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]



def partition(t, p, q):
   pivot = t[q]
   i = p - 1
   
   for j in range(p,q):
       if t[j] < pivot:
           i += 1
           swap(t,i,j)
   swap(t,(i+1),q)

   return i+1



# ─── Tri rapide ───────────────────────────────────────────────────────────────

def quicksort(t, p, q):
    if p < q:
        r = partition(t, p, q)
        quicksort(t, p, r - 1)
        quicksort(t, r + 1, q)


#test
arr = [1, 7, 4, 1, 10, 9, -2]
quicksort(arr, 0, len(arr) - 1)
print(arr)

# ─── Tests ────────────────────────────────────────────────────────────────────

def is_sorted(t):
    return all(t[k] <= t[k + 1] for k in range(len(t) - 1))

def run_tests():
    cas = [
        ("Tableau aléatoire",  random.sample(range(100), 15)),
        ("Déjà trié",          list(range(10))),
        ("Trié à l'envers",    list(range(10, 0, -1))),
        ("Un seul élément",    [42]),
        ("Deux éléments",      [5, 3]),
        ("Doublons",           [4, 2, 4, 1, 2, 3, 4]),
        ("Tous identiques",    [7, 7, 7, 7]),
    ]

    print(f"{'Cas':<22} {'Avant':<35} {'Après':<35} {'OK?'}")
    print("─" * 100)
    for nom, t in cas:
        avant = t.copy()
        quicksort(t, 0, len(t) - 1)
        ok = is_sorted(t) and sorted(avant) == t
        print(f"{nom:<22} {str(avant):<35} {str(t):<35} {'✓' if ok else '✗ ERREUR'}")

print(run_tests())