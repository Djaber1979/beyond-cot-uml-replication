# Beyond Chains-of-Thought: Multi-LLM Voting for Behavioral Augmentation of UML Class Diagrams — Replication

This repository accompanies the article **"Beyond Chains-of-Thought: Multi-LLM Voting for Behavioral Augmentation of UML Class Diagrams"** and provides code, data pointers, and scripts to reproduce the main findings (raw multi‑LLM consensus, CoT self‑consistency, and Post‑CoT consensus; evaluation vs. the expert‑vetted *Consensus‑49*).

## What’s here

- `data/` — input datasets used for reproduction:
  - `Annotation_and_Mapping_Combined.csv` — canonicalized raw proposals with model/run metadata.
  - `consensus_49.csv` — expert‑vetted gold set (49 pairs).
- `src/` — Python code for normalization, consensus construction, and evaluation.
- `artifacts/` — reference outputs (CSV/JSON) used to validate end‑to‑end reproduction (e.g., `universe_916.csv`, `k_sweep_metrics.csv`, `postcot_pairs_k2.csv`, etc.).
- `config/config.yaml` — central configuration (paths and thresholds: `k_raw_consensus=5`, `k_intra=6`, `k_inter=2`).  
- `docs/REPRODUCIBILITY.md` — step‑by‑step guide and expected outputs/checksums.
- CI via GitHub Actions (`.github/workflows/ci.yml`) that installs dependencies and runs smoke tests.

## Quick start

### 1) Environment

```bash
# Option A: Python virtualenv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Option B: Conda
conda env create -f environment.yml
conda activate beyond-cot-uml

# Option C: Docker
docker build -t beyond-cot-uml .
docker run --rm -it -v $(pwd):/work beyond-cot-uml make reproduce
```

### 2) Reproduce the pipeline

```bash
# From repo root
make reproduce
```

This will:
1. Canonicalize input data and construct the 916‑item universe.
2. Build raw multi‑LLM consensus (default `k=5`) and export per‑pair supports and histograms.
3. Compute per‑model CoT self‑consistent cores (`k_intra=6`) and the Post‑CoT consensus (`k_inter=2`).
4. Evaluate candidate sets against *Consensus‑49* and write metrics to `artifacts/summary_metrics.json` & CSVs.

### 3) Expected results (spot checks)

We include reference outputs in `artifacts/` for validation. You can verify integrity by comparing checksums:

```bash
make verify
```

## Human‑in‑the‑loop, Bias, and Ethics

The pipeline foregrounds **human‑in‑the‑loop** curation: experts reconcile near‑synonyms, adjudicate ambiguous placements, and define the gold set (*Consensus‑49*). While inter‑model agreement is informative, **agreement ≠ correctness**. We therefore report accuracy vs. gold and require expert review of contentious cases.  
Potential **biases** may arise from model families, sampling strategies (e.g., CoT prompting), and naming conventions. We provide transparent preprocessing and thresholds in `config/config.yaml` and release metrics enabling sensitivity analyses. Users replicating or extending this work should remain mindful of dataset biases and document any deviations from the provided configuration.

## How to cite

See `CITATION.cff`. If you use the code or data, please cite the article and this repository.

## License

MIT (see `LICENSE`).

---

*Last updated:* 2025-08-23
