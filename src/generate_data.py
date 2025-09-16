import argparse, random
import pandas as pd

def gen_loads(path: str, n=100, min_kw=5, max_kw=150):
    # no seed → system time is used
    data = [{"LoadID": f"L{i+1}", "Demand_kW": random.randint(min_kw, max_kw)} for i in range(n)]
    pd.DataFrame(data).to_csv(path, index=False)

def gen_transformers(path: str, m=10, min_kw=250, max_kw=500):
    data = [{"TransformerID": f"T{j+1}", "Capacity_kW": random.randint(min_kw, max_kw)} for j in range(m)]
    pd.DataFrame(data).to_csv(path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic load/transformer datasets")
    parser.add_argument("--loads_out", default="data/large_loads.csv")
    parser.add_argument("--transformers_out", default="data/large_transformers.csv")
    parser.add_argument("--n_loads", type=int, default=100)
    parser.add_argument("--m_transformers", type=int, default=10)
    parser.add_argument("--load_min", type=int, default=5)
    parser.add_argument("--load_max", type=int, default=150)
    parser.add_argument("--xfmr_min", type=int, default=250)
    parser.add_argument("--xfmr_max", type=int, default=500)
    args = parser.parse_args()

    gen_loads(args.loads_out, n=args.n_loads, min_kw=args.load_min, max_kw=args.load_max)
    gen_transformers(args.transformers_out, m=args.m_transformers, min_kw=args.xfmr_min, max_kw=args.xfmr_max)
    print(f"Wrote {args.loads_out} and {args.transformers_out}")
