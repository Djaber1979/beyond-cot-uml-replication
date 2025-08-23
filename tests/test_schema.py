import os
import pandas as pd

def test_data_files_exist():
    assert os.path.exists('data/Annotation_and_Mapping_Combined.csv')
    assert os.path.exists('data/consensus_49.csv')

def test_min_columns():
    df = pd.read_csv('data/Annotation_and_Mapping_Combined.csv')
    cols = [c.lower() for c in df.columns]
    needed = {'class','method','model','run'}
    assert len(needed.intersection(set(cols))) >= 2  # allow flexible schemas
