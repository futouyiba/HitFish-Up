# -*- coding: utf-8 -*-
"""
Pure-numpy clustering / metric toolkit for the Authoring Archetype probe.

No scipy/sklearn in this environment; everything here is deliberately simple,
transparent and explainable:
- hierarchical clustering (average linkage) over a precomputed distance matrix
- k-medoids (PAM-style, deterministic seeding)
- ARI / NMI for cross-component cluster consistency
- greedy radius-constrained set cover -> compression curve
"""
from __future__ import annotations

import numpy as np
from itertools import combinations


# ---------------------------------------------------------------- distances

def pairwise_l1(X: np.ndarray) -> np.ndarray:
    """Mean absolute difference per dimension -> scalar distance per pair.

    D[i, j] = mean_k |X[i, k] - X[j, k]|   (interpretable: average per-field
    effect difference between two fish on this component).
    """
    n = X.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        diff = np.abs(X[i][None, :] - X)
        D[i] = diff.mean(axis=1)
    return D


# ------------------------------------------------- hierarchical clustering

def _condensed(D: np.ndarray) -> np.ndarray:
    n = D.shape[0]
    iu = np.triu_indices(n, k=1)
    return D[iu]


def _average_linkage(D: np.ndarray) -> tuple[np.ndarray, list]:
    """Naive average-linkage agglomeration.

    Returns (merge_heights, merges) where merges is a list of
    (cluster_a_members, cluster_b_members) in merge order.
    Deterministic: always merges the closest pair, lowest index first on ties.
    """
    n = D.shape[0]
    clusters = {i: [i] for i in range(n)}
    merges = []
    heights = []
    for _ in range(n - 1):
        ids = sorted(clusters)
        best = None
        best_d = np.inf
        for a, b in combinations(ids, 2):
            ma, mb = clusters[a], clusters[b]
            d = D[np.ix_(ma, mb)].mean()
            if d < best_d - 1e-12:
                best_d, best = d, (a, b)
        a, b = best
        clusters[a] = clusters[a] + clusters[b]
        del clusters[b]
        merges.append((a, b))
        heights.append(best_d)
    return np.array(heights), merges


def fcluster_average(D: np.ndarray, threshold: float) -> np.ndarray:
    """Cut the average-linkage tree: clusters whose linkage distance never
    exceeded `threshold` stay together; i.e. cut at first merge with
    height > threshold."""
    n = D.shape[0]
    heights, merges = _average_linkage(D)
    clusters = {i: [i] for i in range(n)}
    for (a, b), h in zip(merges, heights):
        if h > threshold:
            break
        clusters[a] = clusters[a] + clusters[b]
        del clusters[b]
    labels = np.zeros(n, dtype=int)
    for k, members in enumerate(sorted(clusters.values())):
        for m in members:
            labels[m] = k
    return labels


# ---------------------------------------------------------------- k-medoids

def kmedoids(D: np.ndarray, k: int, rng_seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """PAM-style k-medoids with deterministic BUILD seeding.

    Returns (labels, medoid_indices).
    """
    n = D.shape[0]
    k = min(k, n)
    # BUILD phase: first medoid minimises total distance; then greedily add
    # the point that most reduces total nearest-medoid distance.
    medoids = [int(np.argmin(D.sum(axis=1)))]
    while len(medoids) < k:
        best_gain, best_i = -np.inf, None
        for i in range(n):
            if i in medoids:
                continue
            gain = np.minimum(D[:, medoids].min(axis=1), D[:, i]).sum()
            if gain > best_gain:
                best_gain, best_i = gain, i
        medoids.append(best_i)
    medoids = np.array(medoids)
    # SWAP phase: local search until no improving swap
    labels = D[:, medoids].argmin(axis=1)
    cost = D[:, medoids].min(axis=1).sum()
    improved = True
    while improved:
        improved = False
        for mi in range(k):
            for cand in range(n):
                if cand in medoids:
                    continue
                trial = medoids.copy()
                trial[mi] = cand
                c = D[:, trial].min(axis=1).sum()
                if c < cost - 1e-12:
                    medoids, cost, improved = trial, c, True
                    break
            if improved:
                break
    labels = D[:, medoids].argmin(axis=1)
    return labels, medoids


# --------------------------------------------------- compression curve

def greedy_cover(D: np.ndarray, epsilon: float) -> tuple[list[int], np.ndarray]:
    """Greedy set cover: choose medoids so every fish is within `epsilon`
    of some chosen medoid. Returns (medoid_indices, assignment).

    Fish not coverable at all (nearest neighbour > epsilon even alone ->
    cannot happen since d(i,i)=0; but a fish may only cover itself) still get
    assigned to their nearest chosen medoid; coverage counts only fish within
    epsilon.
    """
    n = D.shape[0]
    covered = np.zeros(n, dtype=bool)
    chosen: list[int] = []
    assign = np.full(n, -1, dtype=int)
    while not covered.all():
        # candidate covering most currently-uncovered fish
        reach = D <= epsilon
        gains = (reach & ~covered[None, :]).sum(axis=1)
        # tie-break: prefer candidate whose covered set has smallest total
        # distance (more central) — deterministic via argmax then order.
        best = int(np.argmax(gains))
        chosen.append(best)
        newly = reach[best] & ~covered
        assign[newly] = len(chosen) - 1
        covered |= reach[best]
    # any fish left uncovered by construction (shouldn't happen: itself)
    if (assign == -1).any():
        assign[assign == -1] = 0
    return chosen, assign


# -------------------------------------------------------- ARI / NMI

def _contingency(a: np.ndarray, b: np.ndarray):
    ua, ub = np.unique(a), np.unique(b)
    C = np.zeros((ua.size, ub.size), dtype=np.int64)
    for i, x in enumerate(ua):
        for j, y in enumerate(ub):
            C[i, j] = np.sum((a == x) & (b == y))
    return C, ua, ub


def adjusted_rand_index(a: np.ndarray, b: np.ndarray) -> float:
    C, _, _ = _contingency(a, b)
    n = C.sum()
    comb2 = lambda x: x * (x - 1) / 2.0
    sum_c = comb2(C).sum()
    sum_a = comb2(C.sum(axis=1)).sum()
    sum_b = comb2(C.sum(axis=0)).sum()
    total = comb2(n)
    expected = sum_a * sum_b / total
    max_index = (sum_a + sum_b) / 2.0
    if max_index == expected:
        return 1.0
    return (sum_c - expected) / (max_index - expected)


def normalized_mutual_info(a: np.ndarray, b: np.ndarray) -> float:
    C, _, _ = _contingency(a, b)
    n = C.sum().astype(float)
    P = C / n
    pa = C.sum(axis=1) / n
    pb = C.sum(axis=0) / n
    mi = 0.0
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            if P[i, j] > 0:
                mi += P[i, j] * np.log(P[i, j] / (pa[i] * pb[j]))
    ha = -np.sum(pa[pa > 0] * np.log(pa[pa > 0]))
    hb = -np.sum(pb[pb > 0] * np.log(pb[pb > 0]))
    if ha == 0 or hb == 0:
        return 1.0 if ha == hb else 0.0
    return mi / ((ha + hb) / 2.0)
