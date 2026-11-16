"""Graph-based edge geodesic baseline for triangle meshes."""
if __package__:
    from .geodesics import mesh_edge_distances, mesh_edge_shortest_path
    __all__ = ["mesh_edge_distances", "mesh_edge_shortest_path"]
else:
    __all__ = []
