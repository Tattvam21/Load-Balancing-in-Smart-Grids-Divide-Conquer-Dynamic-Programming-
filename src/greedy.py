from typing import List, Tuple, Dict

def greedy_assign(loads: List[Tuple[str,int]], caps: List[int]):
    """
    Greedy baseline:
    - Sort loads descending by kW
    - Place on transformer with most remaining capacity;
      if none fits, place where overload increase is least (heuristic).
    Returns: assignment dict, remaining capacity list, list of overloaded items
    """
    m = len(caps)
    remaining = caps[:]
    assignment: Dict[int, List[Tuple[str,int]]] = {i: [] for i in range(m)}
    overload_items: List[Tuple[str,int]] = []

    for lid, kw in sorted(loads, key=lambda x: x[1], reverse=True):
        # Pick transformer with most remaining capacity
        idx = max(range(m), key=lambda i: remaining[i])
        if kw <= remaining[idx]:
            assignment[idx].append((lid, kw))
            remaining[idx] -= kw
            continue

        # Try any transformer that currently fits
        placed = False
        for i in sorted(range(m), key=lambda i: remaining[i], reverse=True):
            if kw <= remaining[i]:
                assignment[i].append((lid, kw))
                remaining[i] -= kw
                placed = True
                break

        # If still not placed, put where overload is least (heuristic fallback)
        if not placed:
            idx2 = max(range(m), key=lambda i: remaining[i] - kw)
            assignment[idx2].append((lid, kw))
            remaining[idx2] -= kw
            overload_items.append((lid, kw))

    return assignment, remaining, overload_items
