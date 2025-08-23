import os, yaml, pandas as pd
from src.utils.io import read_csv, write_csv

def self_consistent_sets(pairs_by_model_run: pd.DataFrame, k_intra: int) -> pd.DataFrame:
    # Count per model across runs
    grp = (pairs_by_model_run
           .groupby(['model','class','method'])['run']
           .nunique().reset_index(name='support_runs'))
    grp['kept'] = grp['support_runs'] >= k_intra
    kept = grp[grp['kept']].copy()
    return kept[['model','class','method','support_runs']]

def run(config_path='config/config.yaml'):
    with open(config_path,'r') as f:
        cfg=yaml.safe_load(f)
    out_dir = cfg['paths']['out_dir']
    k_intra = int(cfg['thresholds']['k_intra'])

    pairs = read_csv(os.path.join(out_dir, 'pairs_by_model_run.csv'))
    kept = self_consistent_sets(pairs, k_intra=k_intra)
    write_csv(kept, os.path.join(out_dir, f'self_consistent_k{k_intra}.csv'))

if __name__=='__main__':
    run()
