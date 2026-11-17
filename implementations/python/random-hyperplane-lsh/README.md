# Random-hyperplane locality-sensitive hashing

A small, static, in-memory implementation of multi-table sign random projections for approximate cosine-similarity search.

## Install and test

    python -m pip install -r requirements.txt
    python -m pytest -q

## Example

    import numpy as np
    from random_hyperplane_lsh import RandomHyperplaneLSH

    vectors = np.array([[1., 0.], [.9, .1], [0., 1.], [-1., 0.]])
    index = RandomHyperplaneLSH(n_planes=12, n_tables=8, seed=7).fit(vectors)
    for neighbor in index.query([1., .05], top_k=3):
        print(neighbor.index, neighbor.similarity)

## Contract and limitations

- Input rows and queries must be finite, non-zero vectors with the same feature dimension.
- Vectors are L2-normalized; cosine similarity is the ranking metric.
- Each table hashes signs of random hyperplane projections. A candidate is returned if it collides with the query in at least one table.
- Candidate scores are recomputed exactly, but candidate discovery is approximate. A true nearest neighbour can be missed.
- More tables tend to improve recall while increasing memory and query work. More planes per table tend to make buckets more selective.
- This transparent reference is not a tuned high-dimensional index. It has no persistence, updates, batching, memory budget, recall guarantee or production latency claim.
- It covers only random-hyperplane LSH. HNSW, IVF-PQ and ScaNN remain separate open systems.
