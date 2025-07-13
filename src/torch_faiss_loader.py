#!/usr/bin/env python3

import numpy as np
import faiss

root = "./embedding_database/"
embs_np = np.load(root + "embeddings.npy")    # shape (N, d), dtype float32
ids_np  = np.load(root + "ids.npy")           # shape (N,),      dtype int64


# 3) Build & populate FAISS
d = embs_np.shape[1]
index = faiss.IndexIDMap(faiss.IndexFlatIP(d))
index.add_with_ids(embs_np, ids_np)

# 4) Persist
faiss.write_index(index, root + "faiss_index.faiss")

def search_neighbors(index: faiss.Index, 
                     query_vec: np.ndarray, 
                     k: int = 5
                    ) -> tuple[np.ndarray, np.ndarray]:
    """
    Search the FAISS index for the k nearest neighbors of `query_vec`.

    Args:
      index: a faiss.IndexIDMap(IndexFlatIP) already populated.
      query_vec: 1-D float32 array of length d.
      k: number of neighbors to return.

    Returns:
      distances: 1-D float32 array of length k (inner-product scores).
      ids:       1-D int64   array of length k (your stored IDs).
    """
    # 1) Ensure shape is (1, d)
    q = query_vec.reshape(1, -1).astype("float32")
    # 2) (Re)normalize for cosine similarity
    q /= np.linalg.norm(q, axis=1, keepdims=True) + 1e-12
    # 3) Run the search
    D, I = index.search(q, k)
    return D[0], I[0]


# --- Example usage with your existing index + embeddings ---
# (Assumes you've already done: embs_np = np.load(...), ids_np = np.load(...),
#  index = IndexIDMap(IndexFlatIP(d)); index.add_with_ids(embs_np, ids_np))

# Query with the first stored embedding
first_vec = embs_np[0]        # shape (d,)
distances, neighbor_ids = search_neighbors(index, first_vec, k=5)

print("Querying with embedding #0")
print("Neighbor IDs      :", neighbor_ids)
print("Cosine similarities:", distances)
