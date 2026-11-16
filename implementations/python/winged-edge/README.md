# Winged-edge polygon mesh

Builds a winged-edge representation from consistently oriented polygon faces. Each undirected edge stores canonical endpoints, left/right incident faces, and the predecessor/successor edge on each incident face. A missing incident face denotes a boundary side.

The builder rejects repeated vertices, duplicate faces, inconsistent winding and edges incident to more than two faces. It is a static topology representation: no local editing, automatic orientation repair, geometric intersection checking or non-manifold repair.
