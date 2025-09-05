import os
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_dataset(path: str):
    # CSV expected; adjust if JSON
    df = pd.read_csv(path)
    # normalize columns
    for col in ["Course Title", "Course Description", "Released Languages", "Who This Course is For"]:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    return df

def build_corpus_rows(df: pd.DataFrame):
    rows = []
    for i, r in df.iterrows():
        text = (
            f"Course Title: {r['Course Title']}\n"
            f"About Course: {r['Course Description']}\n"
            f"Course Released Languages: {r['Released Languages']}\n"
            f"Who This Course Is For: {r['Who This Course is For']}"
        )
        rows.append({"id": i, "text": text})
    return rows

def embed_texts(texts, model):
    emb = model.encode(texts, normalize_embeddings=True)
    return np.array(emb, dtype="float32")

def build_or_load_index(df_path: str, idx_dir: str = "data/.index"):
    os.makedirs(idx_dir, exist_ok=True)
    index_file = os.path.join(idx_dir, "courses.faiss")
    meta_file  = os.path.join(idx_dir, "meta.parquet")

    model = SentenceTransformer(EMB_MODEL)
    if os.path.exists(index_file) and os.path.exists(meta_file):
        import pyarrow.parquet as pq
        meta = pq.read_table(meta_file).to_pandas()
        dim = model.get_sentence_embedding_dimension()
        index = faiss.read_index(index_file)
        return meta, index, model

    df = load_dataset(df_path)
    rows = build_corpus_rows(df)
    texts = [r["text"] for r in rows]
    embs = embed_texts(texts, model)
    dim = embs.shape[1]

    index = faiss.IndexFlatIP(dim)  # cosine because we normalized
    index.add(embs)

    # save
    faiss.write_index(index, index_file)
    pd.DataFrame(rows).to_parquet(meta_file, index=False)

    import pyarrow.parquet as pq
    meta = pd.DataFrame(rows)
    return meta, index, model
