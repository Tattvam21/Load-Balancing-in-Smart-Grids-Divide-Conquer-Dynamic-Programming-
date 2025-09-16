# Load Balancing in Smart Grids — Algorithms Project (Python)

Compare a **Greedy heuristic** vs an **Exact Dynamic Programming (Knapsack + Subset-Sum)** approach
for assigning loads to transformers without exceeding capacities and minimizing shed load.

## Project layout

LoadBalancingSmartGrid/
data/                          # CSV input files (sample + generated)
src/                           # algorithms + entry point
results/                       # outputs (metrics + assignments)
report/                        # put your PPT / DOC here
requirements.txt
README.md

## Quick start

1. create env and install deps

```
pip install -r requirements.txt
```

2. run both algorithms on sample data

```
python src/main.py --algo both
```

3. optional: run with your own CSV data

```
python src/main.py --loads data/my_loads.csv --transformers data/my_transformers.csv --algo dp --out results/my_run
```

## Generate synthetic datasets

You can generate random load/transformer datasets for experiments.

Default: 100 loads, 10 transformers

```
python src/generate_data.py
```

Custom: 200 loads, 15 transformers

```
python src/generate_data.py --n_loads 200 --m_transformers 15
```

Adjust ranges (kW)

```
python src/generate_data.py --load_min 10 --load_max 180 --xfmr_min 300 --xfmr_max 600
```

This creates:

* data/large\_loads.csv
* data/large\_transformers.csv

Run algorithms on the generated dataset:

```
python src/main.py --loads data/large_loads.csv --transformers data/large_transformers.csv --algo both --out results/large_run
```

## CSV formats

data/sample\_loads.csv

```
LoadID,Demand_kW
L1,90
L2,75
...
```

data/sample\_transformers.csv

```
TransformerID,Capacity_kW
T1,150
T2,120
...
```

## Sample outputs

After running with `--algo both`, you will see:

* results/large\_run/metrics\_greedy.json → Greedy assignment stats
* results/large\_run/metrics\_dp.json → DP assignment stats
* results/large\_run/assignment.csv → Greedy assignment
* results/dp/large\_run/assignment.csv → DP assignment

Example metrics JSON:

```
{
  "served_kW": 375,
  "shed_kW": 115,
  "max_util": 1.0,
  "avg_util": 0.93,
  "util_stddev": 0.04,
  "per_transformer_kW": [150, 120, 105]
}
```

## Notes

* DP is pseudo-polynomial in total capacity; keep kW integers.
* Greedy may overload transformers; DP never overloads when feasible.
* Outputs are written as JSON (metrics) and CSV (assignments).
