import pandas as pd
import faiss
import numpy as np
from utils import parse_language_codes, filter_by_language_code

def retrieve(query: str, index, model, meta_df, k=5):
    
    #Retrieves the top-k most relevant hits for a given query.
    
    q_emb = model.encode([query], normalize_embeddings=True).astype("float32")
    D, I = index.search(q_emb, k)
    hits = meta_df.iloc[I[0]].copy()
    hits["score"] = D[0]
    return hits

def answer_from_hits(hits_df: pd.DataFrame, raw_df: pd.DataFrame, user_query: str):
    
    #Return multiple matching courses (top-k).
    
    if hits_df.empty:
        return {"Error": ["I couldn’t find a relevant course in the provided dataset."]}

    results = []
    for _, row in hits_df.iterrows():
        idx = row["id"]
        if idx >= len(raw_df):
            continue
        r = raw_df.iloc[idx]

        langs = ", ".join([l for l in parse_language_codes(r["Released Languages"]) if l])

        results.append({
            "Course Title": r["Course Title"],
            "About Course": r["Course Description"],
            "Who This Course Is For": r["Who This Course is For"],
            "Available Languages": langs if langs else "Not specified",
        })

    return results  # return list instead of single dict

def list_courses_in_language(raw_df: pd.DataFrame, lang_code: int):
    
    #Lists all courses available in a given language.
    
    sub = filter_by_language_code(raw_df, lang_code)
    if sub.empty:
        return "No courses found for that language in the dataset."
    
    lines = []
    for _, r in sub.iterrows():
        lines.append(f"- {r['Course Title']}")
    
    return "\n".join(lines)

