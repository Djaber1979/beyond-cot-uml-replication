import os, yaml, pandas as pd
from collections import defaultdict
from src.utils.io import read_csv, write_csv, best_effort_columns
from src.utils.text import canonicalize_class, canonicalize_method

def canonicalize(df, column_map):
    df = best_effort_columns(df, column_map)
    # Ensure required columns exist or create fallbacks
    for col in ['class','method']:
        if col not in df.columns:
            raise ValueError(f'Missing required column: {col}')
    # Optional columns
    if 'model' not in df.columns: df['model'] = 'unknown_model'
    if 'run' not in df.columns: df['run'] = 0

    df['class'] = df['class'].astype(str).map(canonicalize_class)
    df['method'] = df['method'].astype(str).map(canonicalize_method)
    df['model'] = df['model'].astype(str)
    df['run'] = pd.to_numeric(df['run'], errors='coerce').fillna(0).astype(int)
    return df[['class','method','model','run']].dropna()

def construct_universe(df):
    uni = df[['class','method']].drop_duplicates().sort_values(['class','method']).reset_index(drop=True)
    return uni

def pair_model_matrix(df):
    pairs = df[['class','method']].drop_duplicates().reset_index(drop=True)
    models = sorted(df['model'].unique())
    # Indicator per pair per model
    mat = []
    for _, row in pairs.iterrows():
        c,m = row['class'], row['method']
        present = {mo: 0 for mo in models}
        present.update(df[(df['class']==c)&(df['method']==m)].groupby('model').size().astype(int).to_dict())
        mat.append({'class': c, 'method': m, **{mo: int(p>0) for mo,p in present.items()}})
    return pd.DataFrame(mat)

def run(config_path='config/config.yaml'):
    with open(config_path,'r') as f:
        cfg=yaml.safe_load(f)
    in_csv = cfg['paths']['proposals_csv']
    out_dir = cfg['paths']['out_dir']
    colmap = cfg['columns']

    os.makedirs(out_dir, exist_ok=True)

    df = read_csv(in_csv)
    df = canonicalize(df, colmap)

    # Save canonical proposals
    write_csv(df, os.path.join(out_dir, 'pairs_by_model_run.csv'))

    # Universe
    uni = construct_universe(df)
    write_csv(uni, os.path.join(out_dir, 'universe_916.csv'))

    # Pair×Model matrix
    mat = pair_model_matrix(df)
    write_csv(mat, os.path.join(out_dir, 'pair_model_matrix.csv'))

if __name__=='__main__':
    run()
