import os, yaml, pandas as pd
from src.utils.io import read_csv, write_csv

def prf1(candidates: pd.DataFrame, gold: pd.DataFrame):
    cand = set(map(tuple, candidates[['class','method']].dropna().values.tolist()))
    gset = set(map(tuple, gold[['class','method']].dropna().values.tolist()))
    tp = len(cand & gset)
    fp = len(cand - gset)
    fn = len(gset - cand)
    prec = tp / (tp + fp) if (tp+fp) else 0.0
    rec = tp / (tp + fn) if (tp+fn) else 0.0
    f1 = 2*prec*rec / (prec+rec) if (prec+rec) else 0.0
    return {'TP': tp, 'FP': fp, 'FN': fn, 'precision': prec, 'recall': rec, 'f1': f1}

def run(config_path='config/config.yaml'):
    with open(config_path,'r') as f:
        cfg=yaml.safe_load(f)
    out_dir = cfg['paths']['out_dir']
    gold_csv = cfg['paths']['gold_csv']

    gold = read_csv(gold_csv)

    # Evaluate raw consensus (k)
    rawk = read_csv(os.path.join(out_dir, f"raw_consensus_k{cfg['thresholds']['k_raw_consensus']}.csv"))
    m_raw = prf1(rawk, gold)

    # Evaluate post-CoT
    post = read_csv(os.path.join(out_dir, f"postcot_pairs_k{cfg['thresholds']['k_inter']}.csv"))
    m_post = prf1(post, gold)

    # Save summary
    out = {'raw_consensus': m_raw, 'post_cot': m_post}
    import json
    with open(os.path.join(out_dir, 'summary_metrics.json'),'w') as f:
        json.dump(out, f, indent=2)

    # Save CSVs
    pd.DataFrame([m_raw]).to_csv(os.path.join(out_dir, 'metrics_raw_consensus.csv'), index=False)
    pd.DataFrame([m_post]).to_csv(os.path.join(out_dir, 'metrics_postcot.csv'), index=False)

if __name__=='__main__':
    run()
