# Load Balancing in Smart Grids — Algorithms Project (Python)

Compare a **Greedy heuristic** vs an **Exact Dynamic Programming (Knapsack + Subset-Sum)** approach
for assigning loads to transformers without exceeding capacities and minimizing shed load.

## Project layout
```
LoadBalancingSmartGrid/
  data/                      # CSV input files
  src/                       # algorithms + entry point
  results/                   # outputs (metrics + assignments)
  report/                    # put your PPT / DOC here
  requirements.txt
  README.md
```

## Quick start

```bash
# 1) create env and install deps
pip install -r requirements.txt

# 2) run both algorithms on sample data
python src/main.py --algo both

# Optional: use your own data
python src/main.py --loads data/my_loads.csv --transformers data/my_transformers.csv --algo dp --out results/my_run
```

### CSV formats

`data/sample_loads.csv`
```
LoadID,Demand_kW
L1,90
L2,75
...
```

`data/sample_transformers.csv`
```
TransformerID,Capacity_kW
T1,150
T2,120
...
```

## Notes
- DP is pseudo‑polynomial in total capacity; keep kW integers.
- Greedy may overload transformers; DP never overloads when feasible.
- Outputs: `results/metrics_*.json` and `results/assignment.csv`.
