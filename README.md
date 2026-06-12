# Customer Support Ticket Clusterization

Unsupervised clustering of customer support tickets to discover complaint and error patterns — simulating the **feedback-to-data flywheel** concept from production ML systems.

## Goal

Given ~8,500 real-world-style support tickets, find meaningful groups of similar issues **without labels** and extract actionable insights:

1. **Ticket Clustering** — group tickets by problem type using text embeddings, so a team can see "what breaks most often" at a glance
2. **Customer Segmentation** — group customers by support behavior (frequency, issue types, satisfaction) to identify who needs the most attention

## Dataset

[Kaggle — Customer Support Ticket Dataset](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset): 8,469 tickets, 17 features (type, subject, description, priority, channel, product, satisfaction, etc.).

## Approach

| Phase | What | Notebook |
|-------|------|----------|
| EDA | Distributions, missing values, text analysis, cross-tabulations | `01_eda.ipynb` |
| Preprocessing | Template substitution, text cleaning, drop noise columns |  |
| Feature Engineering | TF-IDF (baseline) and SBERT embeddings + UMAP dimensionality reduction |  |
| Clustering | KMeans and HDBSCAN on UMAP-reduced embeddings, elbow/silhouette selection |  |
| Customer Segmentation | Aggregate per-customer features, segment with KMeans/HDBSCAN |  |

## Key methods

- **Text embeddings**: `all-MiniLM-L6-v2` (SBERT, 384-dim) — captures semantic similarity between ticket descriptions
- **Dimensionality reduction**: UMAP to 50d for clustering, 2d for visualization
- **Clustering**: KMeans (parametric) + HDBSCAN (density-based, no need to pick k)
- **Validation**: semi-supervised — compare clusters against Ticket Subject (16 categories) using ARI/AMI

## Project structure

```
notebooks/          # Jupyter notebooks (EDA, preprocessing, clustering, analysis)
src/                # Reusable Python modules (data loading, preprocessing, clustering)
data/               # Raw CSV (not tracked in git)
reports/            # Generated outputs and visualizations
```

## Setup

```bash
python3 -m venv .ticketcluster
source .ticketcluster/bin/activate
pip install -r requirements.txt
```

Place `customer_support_tickets.csv` into the `data/` directory.

## Current status

- [x] Phase 1 — Environment setup
- [x] Phase 2 — EDA
- [ ] Phase 3 — Preprocessing
- [ ] Phase 4 — Feature engineering
- [ ] Phase 5 — Clustering
- [ ] Phase 6 — Customer segmentation
