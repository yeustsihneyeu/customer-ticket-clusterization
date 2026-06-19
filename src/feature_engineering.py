from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sentence_transformers import SentenceTransformer
from config import DATA_DIR
from sklearn.preprocessing import OneHotEncoder
import umap
from sklearn.decomposition import PCA
from config import RANDOM_SEED

def vectorize_tfidf(descriptions, max_features=5000, ngram_range=(1, 2)):
    vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=ngram_range)
    X = vectorizer.fit_transform(descriptions).toarray() # type: ignore
    return X, vectorizer


def embed_sbert(descriptions, cache_path=DATA_DIR / "sbert_embeddings.npy",
                 model_name="all-MiniLM-L6-v2", force_recompute=False):
    if cache_path.exists() and not force_recompute:
        embeddings = np.load(cache_path)
        if embeddings.shape[0] == len(descriptions):
            return embeddings

    model = SentenceTransformer(model_name)
    embeddings = model.encode(descriptions.tolist(), show_progress_bar=True)
    np.save(cache_path, embeddings)
    return embeddings


def build_combined_features(
        sbert_embeddings, 
        df, 
        categorical_cols=["Ticket Type", "Product Purchased", "Ticket Priority"],
        categorical_weight=1.0):
    
    encoder = OneHotEncoder(sparse_output=False)
    cat_block = encoder.fit_transform(df[categorical_cols])
    cat_block = cat_block * categorical_weight
    return np.hstack([sbert_embeddings, cat_block])


def reduce_umap(X, n_components=50, random_state=RANDOM_SEED):
    reducer = umap.UMAP(n_components=n_components, random_state=random_state)
    return reducer.fit_transform(X)


def reduce_pca(X, n_components=50, random_state=RANDOM_SEED):
    reducer = PCA(n_components=n_components, random_state=random_state)
    return reducer.fit_transform(X)