from typing import List, Tuple, Dict

def _dp_select_subset(loads: List[Tuple[str,int]], total_cap: int) -> List[Tuple[str,int]]:
    """
    0/1 Knapsack specialized where value = weight = kW.
    Maximizes served kW under total capacity.
    Returns the selected subset of loads.
    Time: O(n * total_cap), Memory: O(total_cap)
    """
    n = len(loads)
    dp = [0]*(total_cap+1)
    take = [[False]*(total_cap+1) for _ in range(n)]

    for i, (_, w) in enumerate(loads):
        for c in range(total_cap, w-1, -1):
            if dp[c-w] + w > dp[c]:
                dp[c] = dp[c-w] + w
                take[i][c] = True

    c = max(range(total_cap+1), key=lambda x: dp[x])
    selected: List[Tuple[str,int]] = []
    for i in range(n-1, -1, -1):
        if take[i][c]:
            selected.append(loads[i])
            c -= loads[i][1]
    selected.reverse()
    return selected

def _subset_sum_fill(items: List[Tuple[str,int]], cap: int):
    """
    Best fill up to 'cap' using subset-sum DP.
    Returns (chosen_items, remaining_items)
    """
    n = len(items)
    dp = [0]*(cap+1)
    parent = [[False]*(cap+1) for _ in range(n)]
    for i, (_, w) in enumerate(items):
        for c in range(cap, w-1, -1):
            if dp[c-w] + w > dp[c]:
                dp[c] = dp[c-w] + w
                parent[i][c] = True
    c = max(range(cap+1), key=lambda x: dp[x])
    chosen, used = [], [False]*n
    for i in range(n-1, -1, -1):
        if parent[i][c]:
            chosen.append(items[i]); used[i] = True; c -= items[i][1]
    chosen.reverse()
    remaining = [items[i] for i in range(n) if not used[i]]
    return chosen, remaining

def dp_load_balancing(loads: List[Tuple[str,int]], caps: List[int]):
    """
    Pipeline:
    1) Fleet-level subset via 0/1-knapsack to maximize served kW under sum(caps)
    2) Pack selected loads per transformer using subset-sum DP (no overload)
    Returns: assignment dict, shed_kW, unplaced_items (if packing impossible)
    """
    total_cap = sum(caps)
    selected = _dp_select_subset(loads, total_cap)

    items = selected[:]
    assignment: Dict[int, List[Tuple[str,int]]] = {}
    for j, cap in enumerate(caps):
        chosen, items = _subset_sum_fill(items, cap)
        assignment[j] = chosen

    served = sum(w for lst in assignment.values() for _, w in lst)
    total_load = sum(w for _, w in loads)
    shed = total_load - served
    unplaced = items
    return assignment, shed, unplaced
