#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(".")
DATA = ROOT / "data"
ART = ROOT / "artifacts"

u_csv = DATA / "Annotation_and_Mapping_Combined.csv"
cons54 = DATA / "consensus_54.csv"
cons49 = DATA / "consensus_49.csv"
pair_model = ART / "pair_model_matrix.csv"
boot_path = ART / "bootstrap_jaccard.csv"

k_sweep_out = ART / "k_sweep_metrics.csv"
jaccard_summary_out = ART / "bootstrap_jaccard_summary.csv"
recalc_diff = ART / "RECALC_DIFF.md"

def read_csv_required(p: Path) -> pd.DataFrame:
    if not p.exists():
        raise FileNotFoundError(f"[fatal] missing required file: {p}")
    return pd.read_csv(p)

def compute_prf_vs_consensus(k_values, pair_model_df, cons49_df):
    cols = [c for c in pair_model_df.columns if c.lower().startswith("model")]
    pair_model_df["support"] = pair_model_df[cols].sum(axis=1)
    key = "pair" if "pair" in pair_model_df.columns else "pair_id" if "pair_id" in pair_model_df.columns else None
    if key is None:
        if {"Class","Method"}.issubset(pair_model_df.columns):
            pair_model_df["pair_key"] = pair_model_df["Class"].str.lower().str.strip() + "::" + pair_model_df["Method"].str.lower().str.strip()
            key = "pair_key"
        else:
            raise ValueError("[fatal] Could not infer pair key in pair_model_matrix.csv")

    cons49_keys = set((cons49_df["Class"].str.lower().str.strip() + "::" + cons49_df["Method"].str.lower().str.strip()).tolist())

    rows = []
    for k in k_values:
        cge = set(pair_model_df.loc[pair_model_df["support"]>=k, key].tolist())
        tp = len(cge & cons49_keys)
        fp = len(cge - cons49_keys)
        fn = len(cons49_keys - cge)
        prec = 0.0 if (tp+fp)==0 else 100.0 * tp / (tp+fp)
        rec  = 0.0 if (tp+fn)==0 else 100.0 * tp / (tp+fn)
        f1   = 0.0 if (prec+rec)==0 else 2*prec*rec/(prec+rec)
        rows.append({"k":k, "coverage": len(cge),
                     "precision": round(prec,2), "recall": round(rec,2), "f1": round(f1,2),
                     "TP":tp,"FP":fp,"FN":fn})
    return pd.DataFrame(rows)

def summarize_bootstrap_means(boot_csv_path: Path):
    df = read_csv_required(boot_csv_path)
    k_col = "k" if "k" in df.columns else "threshold"
    j_col = "jaccard_to_full" if "jaccard_to_full" in df.columns else "jaccard"
    g = df.groupby(k_col)[j_col].mean().reset_index()
    g.columns = ["k", "mean_jaccard"]
    g["mean_jaccard"] = g["mean_jaccard"].astype(float).round(3)
    return g

recalc_lines = []

u_df = read_csv_required(u_csv)
cons54_df = read_csv_required(cons54)
cons49_df = read_csv_required(cons49)
pm_df = read_csv_required(pair_model)

k_vals = [2,3,4,5,6,7,8,9]
ks_df = compute_prf_vs_consensus(k_vals, pm_df, cons49_df)
ks_df.to_csv(k_sweep_out, index=False)

if boot_path.exists():
    jacc_df = summarize_bootstrap_means(boot_path)
else:
    jacc_df = pd.DataFrame({"k":k_vals, "mean_jaccard":[np.nan]*len(k_vals)})
    recalc_lines.append("- bootstrap_jaccard.csv missing: mean_jaccard left as NaN (no fabrication).")

jacc_df.to_csv(jaccard_summary_out, index=False)

expected_cov = {2:274, 3:152, 4:102, 5:54, 6:35, 7:21, 8:13, 9:4}
expected_p  = {2:17.88, 3:32.24, 4:48.04, 5:90.74, 6:88.57, 7:90.48, 8:92.31, 9:100.00}
expected_r  = {2:100.00,3:100.00,4:100.00,5:100.00,6:63.27,7:38.78,8:24.49,9:8.16}
expected_f1 = {2:30.34, 3:48.76, 4:64.90, 5:95.15, 6:73.81, 7:54.29, 8:38.71, 9:15.09}
expected_j  = {2:0.498, 3:0.559, 4:0.590, 5:0.559, 6:0.563, 7:0.568, 8:0.571, 9:0.566}

def cmp_map(series, expected, name, tol=0.01):
    diffs = []
    for k in expected:
        got = float(series.loc[series["k"]==k][name])
        exp = expected[k]
        if np.isnan(got):
            diffs.append((k, "NaN", exp))
        elif abs(got-exp) > tol:
            diffs.append((k, got, exp))
    return diffs

d_cov = cmp_map(ks_df, expected_cov, "coverage", tol=0.5)
d_p   = cmp_map(ks_df, expected_p,   "precision", tol=0.05)
d_r   = cmp_map(ks_df, expected_r,   "recall",    tol=0.05)
d_f1  = cmp_map(ks_df, expected_f1,  "f1",        tol=0.05)

if d_cov or d_p or d_r or d_f1:
    recalc_lines.append("## PRF sweep diffs vs manuscript")
for tag, diffs in [("coverage", d_cov), ("precision", d_p), ("recall", d_r), ("f1", d_f1)]:
    if diffs:
        recalc_lines.append(f"- {tag} diffs (k, got, expected): {diffs}")

if boot_path.exists():
    jacc_df = pd.read_csv(jaccard_summary_out)
    d_j = cmp_map(jacc_df, expected_j, "mean_jaccard", tol=0.002)
    if d_j:
        recalc_lines.append("## Bootstrap Jaccard mean diffs vs manuscript")
        recalc_lines.append(f"- mean_jaccard diffs (k, got, expected): {d_j}")
else:
    recalc_lines.append("- Skipped Jaccard diff (no bootstrap_jaccard.csv present)")

if recalc_lines:
    recalc_diff.write_text("\n".join(recalc_lines))
    print("[warn] Wrote diffs to artifacts/RECALC_DIFF.md")
else:
    print("[ok] All manuscript values matched within tolerances.")
