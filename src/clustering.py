import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from kneed import KneeLocator
from config import RANDOM_SEED
import hdbscan
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score


def find_optimal_k(X, k_range):
    results = {"k": [], "inertia": [], "silhouette": [], "calinski_harabasz": [], "davies_bouldin": []}

    for k in k_range:
        model = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_SEED).fit(X)
        labels = model.labels_
        results["k"].append(k)
        results["inertia"].append(model.inertia_)
        results["silhouette"].append(silhouette_score(X, labels))
        results["calinski_harabasz"].append(calinski_harabasz_score(X, labels))
        results["davies_bouldin"].append(davies_bouldin_score(X, labels))

    kneedle = KneeLocator(results["k"], results["inertia"], curve="convex", direction="decreasing")
    results["elbow_k"] = kneedle.elbow # type: ignore

    return results


def run_kmeans(X, n_clusters):
    model = KMeans(n_clusters=n_clusters, n_init=10, random_state=RANDOM_SEED).fit(X)
    return model.labels_, model


def run_hdbscan(X, min_cluster_size):
    model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size).fit(X)
    return model.labels_, model


def evaluate_clustering(X, labels, true_labels=None):
    metrics = {}

    mask = labels != -1
    metrics["noise_ratio"] = 1 - mask.sum() / len(labels)

    n_clusters = len(set(labels[mask]))
    if n_clusters >= 2:
        metrics["silhouette"] = silhouette_score(X[mask], labels[mask])
        metrics["calinski_harabasz"] = calinski_harabasz_score(X[mask], labels[mask])
        metrics["davies_bouldin"] = davies_bouldin_score(X[mask], labels[mask])
    else:
        metrics["silhouette"] = None
        metrics["calinski_harabasz"] = None
        metrics["davies_bouldin"] = None

    if true_labels is not None:
        metrics["ari"] = adjusted_rand_score(true_labels, labels)
        metrics["ami"] = adjusted_mutual_info_score(true_labels, labels)

    return metrics