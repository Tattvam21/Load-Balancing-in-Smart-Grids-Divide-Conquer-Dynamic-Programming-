from typing import List, Tuple, Dict
import pandas as pd
import os, statistics as st

def load_data(load_file: str, transformer_file: str):
    loads_df = pd.read_csv(load_file)
    trans_df = pd.read_csv(transformer_file)
    loads = [(str(row["LoadID"]), int(row["Demand_kW"])) for _, row in loads_df.iterrows()]
    caps  = [int(row["Capacity_kW"]) for _, row in trans_df.iterrows()]
    return loads, caps

def summarize(assignment: Dict[int, List[Tuple[str,int]]], caps: List[int], total_load: int):
    per = [sum(w for _, w in assignment.get(i, [])) for i in range(len(caps))]
    util = [per[i]/caps[i] for i in range(len(caps))]
    return {
        "served_kW": sum(per),
        "shed_kW": total_load - sum(per),
        "max_util": max(util) if util else 0.0,
        "avg_util": sum(util)/len(util) if util else 0.0,
        "util_stddev": st.pstdev(util) if len(util) > 1 else 0.0,
        "per_transformer_kW": per
    }

def save_assignment(assignment: Dict[int, List[Tuple[str,int]]], out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for tid, items in assignment.items():
        for lid, kw in items:
            rows.append({"TransformerIndex": tid, "LoadID": lid, "Assigned_kW": kw})
    df = pd.DataFrame(rows)
    out_path = os.path.join(out_dir, "assignment.csv")
    df.to_csv(out_path, index=False)
    return out_path
