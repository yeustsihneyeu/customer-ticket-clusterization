import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud

def plot_cluster_sizes(labels, save_path=None):
    unique, counts = np.unique(labels, return_counts=True)
    order = np.argsort(-counts)
    unique, counts = unique[order], counts[order]

    colors = ["lightgray" if u == -1 else "steelblue" for u in unique]
    labels_str = ["Noise" if u == -1 else str(u) for u in unique]

    plt.figure(figsize=(14, 5))
    plt.bar(labels_str, counts, color=colors)
    plt.xlabel("Cluster")
    plt.ylabel("Size")
    plt.title("Cluster sizes")
    plt.xticks(rotation=90)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=120)
    plt.show()


def plot_umap_scatter(X_2d, labels, title="", save_path=None):
    labels_str = ["Noise" if l == -1 else str(l) for l in labels]

    fig = px.scatter(
        x=X_2d[:, 0], y=X_2d[:, 1],
        color=labels_str,
        color_discrete_map={"Noise": "lightgray"},
        title=title,
        opacity=0.7,
    )
    fig.update_traces(marker=dict(size=5))

    fig.show()
    if save_path:
        fig.write_image(save_path)

    return fig



def plot_cluster_category_distribution(df, labels, category_col, cluster_id=None, save_path=None):
    cluster_labels = pd.Series(["Noise" if l == -1 else str(l) for l in labels], index=df.index)

    if cluster_id is not None:
        cid = "Noise" if cluster_id == -1 else str(cluster_id)
        counts = df.loc[cluster_labels == cid, category_col].value_counts()

        plt.figure(figsize=(10, 5))
        counts.plot(kind="bar", color="steelblue")
        plt.title(f"{category_col} distribution — cluster {cid}")
        plt.ylabel("Count")
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=120)
        plt.show()
        return counts.to_frame(name="count")

    crosstab = pd.crosstab(cluster_labels, df[category_col], normalize="index")

    plt.figure(figsize=(12, max(6, len(crosstab) * 0.3)))
    sns.heatmap(crosstab, cmap="viridis")
    plt.title(f"{category_col} distribution per cluster (row-normalized)")
    plt.xlabel(category_col)
    plt.ylabel("Cluster")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=120)
    plt.show()
    return crosstab


def top_terms_per_cluster(X_tfidf, labels, vectorizer, top_n=15):
    feature_names = vectorizer.get_feature_names_out()
    result = {}

    for cluster_id in sorted(set(labels)):
        if cluster_id == -1:
            continue
        mean_scores = X_tfidf[labels == cluster_id].mean(axis=0)
        top_idx = mean_scores.argsort()[::-1][:top_n]
        result[cluster_id] = [(feature_names[i], mean_scores[i]) for i in top_idx]

    return result



def plot_cluster_wordcloud(cluster_id, terms_with_scores, save_path=None):
    weights = dict(terms_with_scores)
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(weights)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Cluster {cluster_id} — top terms")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=120)
    plt.show()
    return wc


def find_representative_tickets(X, labels, df, text_col="Ticket Description", n=3):
    result = {}

    for cluster_id in sorted(set(labels)):
        if cluster_id == -1:
            continue
        cluster_mask = labels == cluster_id
        centroid = X[cluster_mask].mean(axis=0)
        dists = np.linalg.norm(X[cluster_mask] - centroid, axis=1)

        nearest_order = np.argsort(dists)[:n]
        positional_idx = np.where(cluster_mask)[0][nearest_order]
        result[cluster_id] = positional_idx.tolist()

    return result


def build_cluster_summary_table(df, labels, X, vectorizer, X_tfidf, top_n_terms=10, n_representative=3):
    terms_by_cluster = top_terms_per_cluster(X_tfidf, labels, vectorizer, top_n=top_n_terms)
    representatives = find_representative_tickets(X, labels, df, n=n_representative)

    rows = []
    for cluster_id in sorted(set(labels)):
        mask = labels == cluster_id
        size = mask.sum()
        top_type = df.loc[mask, "Ticket Type"].mode().iloc[0]

        row = {
            "cluster_id": cluster_id,
            "size": size,
            "pct_of_total": size / len(labels) * 100,
            "top_terms": None,
            "top_ticket_type": top_type,
            "top_ticket_subject": df.loc[mask, "Ticket Subject"].mode().iloc[0],
            "top_product": df.loc[mask, "Product Purchased"].mode().iloc[0],
            "dominant_category_share": (df.loc[mask, "Ticket Type"] == top_type).mean(),
            "avg_satisfaction": df.loc[mask, "Customer Satisfaction Rating"].mean(),
            "representative_ticket_ids": None,
        }

        if cluster_id != -1:
            row["top_terms"] = "; ".join(term for term, score in terms_by_cluster[cluster_id])
            rep_ids = df.iloc[representatives[cluster_id]]["Ticket ID"]
            row["representative_ticket_ids"] = "; ".join(str(t) for t in rep_ids)

        rows.append(row)

    return pd.DataFrame(rows)