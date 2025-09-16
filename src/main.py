import argparse, os, json
from utils import load_data, summarize, save_assignment
from greedy import greedy_assign
from dp import dp_load_balancing

def run(loads_path: str, transformers_path: str, algo: str, out_dir: str):
    loads, caps = load_data(loads_path, transformers_path)
    total = sum(w for _, w in loads)

    if algo.lower() == "greedy":
        assignment, remaining, overloaded = greedy_assign(loads, caps)
        # Note: greedy can overload; served can exceed caps (interpretation-specific)
        metrics = summarize(assignment, caps, total)
        metrics["overloaded_items"] = len(overloaded)
    elif algo.lower() == "dp":
        assignment, shed, unplaced = dp_load_balancing(loads, caps)
        metrics = summarize(assignment, caps, total)
        metrics["unplaced_after_pack"] = len(unplaced)
    elif algo.lower() == "both":
        # run both and write separate files
        g_assignment, g_remaining, g_over = greedy_assign(loads, caps)
        d_assignment, d_shed, d_unplaced = dp_load_balancing(loads, caps)

        g_metrics = summarize(g_assignment, caps, total)
        g_metrics["overloaded_items"] = len(g_over)

        d_metrics = summarize(d_assignment, caps, total)
        d_metrics["unplaced_after_pack"] = len(d_unplaced)

        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "metrics_greedy.json"), "w") as f:
            json.dump(g_metrics, f, indent=2)
        with open(os.path.join(out_dir, "metrics_dp.json"), "w") as f:
            json.dump(d_metrics, f, indent=2)

        g_csv = save_assignment(g_assignment, out_dir)
        d_csv = save_assignment(d_assignment, out_dir.replace("results", "results/dp"))
        print("Greedy metrics:", json.dumps(g_metrics, indent=2))
        print("DP metrics    :", json.dumps(d_metrics, indent=2))
        print("Greedy assignment CSV:", g_csv)
        print("DP assignment CSV:", d_csv)
        return

    # single algo branch
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, f"metrics_{algo.lower()}.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    csv_path = save_assignment(assignment, out_dir)
    print(json.dumps(metrics, indent=2))
    print("Assignment CSV:", csv_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Grid Load Balancing (Greedy vs DP)")
    parser.add_argument("--loads", default="data/sample_loads.csv", help="Path to loads CSV")
    parser.add_argument("--transformers", default="data/sample_transformers.csv", help="Path to transformers CSV")
    parser.add_argument("--algo", default="both", choices=["greedy", "dp", "both"], help="Algorithm to run")
    parser.add_argument("--out", default="results", help="Output directory")
    args = parser.parse_args()
    run(args.loads, args.transformers, args.algo, args.out)
