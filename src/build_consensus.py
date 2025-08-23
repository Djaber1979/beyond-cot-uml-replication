import os, yaml, pandas as pd
from src.utils.io import read_csv, write_csv

def compute_votes(pairs_by_model_run: pd.DataFrame) -> pd.DataFrame:
    # Count distinct models supporting each pair
    votes = (pairs_by_model_run
             .groupby(['class','method'])['model']
             .nunique().reset_index(name='vote_models'))
    return votes.sort_values('vote_models', ascending=False)

def k_filter(votes: pd.DataFrame, k: int) -> pd.DataFrame:
    return votes[votes['vote_models']>=k].sort_values(['class','method']).reset_index(drop=True)

def run(config_path='config/config.yaml'):
    with open(config_path,'r') as f:
        cfg=yaml.safe_load(f)
    out_dir = cfg['paths']['out_dir']
    k = int(cfg['thresholds']['k_raw_consensus'])

    pairs = read_csv(os.path.join(out_dir, 'pairs_by_model_run.csv'))
    votes = compute_votes(pairs)
    write_csv(votes, os.path.join(out_dir, 'pair_model_votes.csv'))

    kset = k_filter(votes, k)
    write_csv(kset, os.path.join(out_dir, f'raw_consensus_k{k}.csv'))

    # Histogram of votes
    hist = votes['vote_models'].value_counts().sort_index().reset_index()
    hist.columns = ['vote_models','num_pairs']
    write_csv(hist, os.path.join(out_dir, 'vote_count_histogram.csv'))

if __name__=='__main__':
    run()
