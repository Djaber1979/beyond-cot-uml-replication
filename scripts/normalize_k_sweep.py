#!/usr/bin/env python3
from pathlib import Path
import pandas as pd

p = Path("artifacts/k_sweep_metrics.csv")
if not p.exists():
    raise SystemExit("[fatal] artifacts/k_sweep_metrics.csv not found")

df = pd.read_csv(p)

for col in ["precision", "recall", "f1"]:
    if col not in df.columns:
        raise SystemExit(f"[fatal] missing column: {col}")
    mask = df[col] <= 1.0
    df.loc[mask, col] = df.loc[mask, col] * 100.0
    df[col] = df[col].astype(float).round(2)

if "coverage" in df.columns and "k" in df.columns:
    cov_map = df.set_index("k")["coverage"].to_dict()
    expected = {2:274, 3:152, 4:102, 5:54, 6:35, 7:21, 8:13, 9:4}
    mismatch = {k:(cov_map.get(k),v) for k,v in expected.items() if cov_map.get(k) != v}
    if mismatch:
        print("[warn] Coverage differs from manuscript in rows:", mismatch)

df.to_csv(p, index=False)
print("[ok] Normalized P/R/F1 to percent in artifacts/k_sweep_metrics.csv")
