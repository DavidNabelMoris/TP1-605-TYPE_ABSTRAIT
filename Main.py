import random

# ─── Assertions axiomatiques & Checkers ───────────────────────────────────────────────────

def assert_check(condition, message):
    if not condition:
        raise AssertionError(f"[VIOLATION] {message}")



def precondition_partition(t, p, q):
    return 0 <= p <= q < len(t)


def post_partition(t, p, q, r):
    pivot = t[r]
    return (
        all(t[k] < pivot for k in range(p, r)) and
        all(t[k] >= pivot for k in range(r + 1, q + 1))
    )


def swap(t, i, j):
    t[i], t[j] = t[j], t[i]

def invariant_partition(t, p, i, j, pivot):
    return (
        all(t[k] < pivot for k in range(p, i+1)) and
        all(t[k] >= pivot for k in range(i+1, j))
    )


# ─── Procédure PARTITION alternative ──────────────────────────────────────────

def partition(t, p, q):
   assert_check(precondition_partition(t, p, q), "Précondition non respectée")
   pivot = t[q]
   i = p - 1
   
   for j in range(p,q):
       assert_check(invariant_partition(t, p, i, j, pivot), "Invariant violé")
       if t[j] < pivot:
           i += 1
           swap(t,i,j)
   r = i + 1
   swap(t,r,q)
   assert_check(post_partition(t, p, q, r), "Postcondition violée")

   return r


# ─── Tri rapide ───────────────────────────────────────────────────────────────

def quicksort(t, p, q):
    if p < q:
        r = partition(t, p, q)
        quicksort(t, p, r - 1)
        quicksort(t, r + 1, q)

def partition_pairs(t, p, q):
    pivot = t[q][0]
    i = p - 1

    for j in range(p, q):
        if t[j][0] < pivot:
            i += 1
            swap(t, i, j)

    swap(t, i + 1, q)
    return i + 1

def quicksort_pairs(t, p, q):
    if p < q:
        r = partition_pairs(t, p, q)
        quicksort_pairs(t, p, r - 1)
        quicksort_pairs(t, r + 1, q)

def stabilized_sort(t):
    arr = [(value, index) for index, value in enumerate(t)]
    quicksort_pairs(arr, 0, len(arr) - 1)
    arr.sort(key=lambda x: (x[0], x[1]))
    return [x[0] for x in arr]

# ─── SSC ────────────────────────────────────────────────────────────────────

def SSC(t, j):
    assert_check(0 <= j < len(t), "Indice j invalide")

    l = j
    while l < len(t) - 1 and t[l] <= t[l + 1]:
        l += 1

    return j, l

# ─── Tri Fusion ────────────────────────────────────────────────────────────────────

def fusion(t, i, k):
    assert_check(0 <= i < k < len(t), "Indices invalides")

    left = t[:i + 1]
    right = t[i + 1:k + 1]

    res = []
    a = b = 0

    while a < len(left) and b < len(right):
        if left[a] <= right[b]:
            res.append(left[a])
            a += 1
        else:
            res.append(right[b])
            b += 1

    res += left[a:]
    res += right[b:]

    t[:k + 1] = res

    assert_check(all(t[x] <= t[x + 1] for x in range(k)), "Fusion incorrecte")

# ─── Tri Intervalles ────────────────────────────────────────────────────────────────────

def interval_sort(t):
    n = len(t)
    if n <= 1:
        return t

    while True:
        i = 0
        merge = False

        while i < n - 1:
            j1, l1 = SSC(t, i)

            if l1 == n - 1:
                break

            j2, l2 = SSC(t, l1 + 1)

            fusion(t, l1, l2)
            merge = True

            i = 0

        if not merge:
            break

    return t


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

    with open("resultats_tests.txt", "w", encoding="utf-8") as f:
        def write(line=""):
            f.write(line + "\n")

        write(f"{'Cas':<22} {'Avant':<35} {'TriRapid':<35} {'Fusion':<35} {'Intervalles':<35} {'OK?'}")
        write("─" * 160)

        for nom, t in cas:
            avant = t.copy()

            t1 = t.copy()
            t2 = t.copy()
            t3 = t.copy()

            quicksort(t1, 0, len(t1) - 1)
            fusion = stabilized_sort(t2)
            interval_sort(t3)

            ok = (
                is_sorted(t1) and
                is_sorted(fusion) and
                is_sorted(t3) and
                sorted(avant) == t1 == fusion == t3
            )

            write(f"{nom:<22} {str(avant):<35} {str(t1):<35} {str(fusion):<35} {str(t3):<35} {'✓' if ok else '✗ ERREUR'}")

    return "Résultats écrits dans resultats_tests.txt"

run_tests()