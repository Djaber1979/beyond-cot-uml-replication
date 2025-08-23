import os, yaml, pandas as pd
from src.utils.io import read_csv, write_csv

def postcot_consensus(self_consistent: pd.DataFrame, k_inter: int) -> pd.DataFrame:
    votes = (self_consistent
             .groupby(['class','method'])['model']
             .nunique().reset_index(name='vote_models'))
    sel = votes[votes['vote_models']>=k_inter].sort_values(['class','method']).reset_index(drop=True)
    return sel

def run(config_path='config/config.yaml'):
    with open(config_path,'r') as f:
        cfg=yaml.safe_load(f)
    out_dir = cfg['paths']['out_dir']
    k_inter = int(cfg['thresholds']['k_inter'])

    sc = read_csv(os.path.join(out_dir, f"self_consistent_k{cfg['thresholds']['k_intra']}.csv"))
    post = postcot_consensus(sc, k_inter=k_inter)
    write_csv(post, os.path.join(out_dir, f'postcot_pairs_k{k_inter}.csv'))

if __name__=='__main__':
    run()
