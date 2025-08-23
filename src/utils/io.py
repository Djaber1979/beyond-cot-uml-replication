import pandas as pd
from typing import Dict, List

def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def write_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)

def best_effort_columns(df: pd.DataFrame, mapping: Dict[str, List[str]]) -> pd.DataFrame:
    lower = {c.lower(): c for c in df.columns}
    out = {}
    for std, aliases in mapping.items():
        for a in aliases:
            if a.lower() in lower:
                out[std] = lower[a.lower()]
                break
    # If already present
    for k in ('class','method','model','run'):
        if k in df.columns:
            out[k] = k
    return df.rename(columns=out)
