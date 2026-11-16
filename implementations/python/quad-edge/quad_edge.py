"""Guibas-Stolfi quad-edge primitives for planar subdivisions.

This module implements the core algebraic topology operators, not a complete
Delaunay triangulator or a geometric embedding/robust-predicate layer.
"""
from dataclasses import dataclass
from typing import Any


@dataclass(eq=False)
class Dart:
    rot: "Dart | None" = None
    onext: "Dart | None" = None
    origin: Any = None
    primal: bool = True

    @property
    def sym(self):
        return self.rot.rot

    @property
    def invrot(self):
        return self.rot.rot.rot

    @property
    def o_prev(self):
        return self.rot.onext.rot

    @property
    def d_next(self):
        return self.sym.onext.sym

    @property
    def d_prev(self):
        return self.invrot.onext.invrot

    @property
    def l_next(self):
        return self.invrot.onext.rot

    @property
    def l_prev(self):
        return self.onext.sym

    @property
    def r_next(self):
        return self.rot.onext.invrot

    @property
    def r_prev(self):
        return self.sym.onext

    @property
    def destination(self):
        return self.sym.origin


@dataclass
class QuadEdge:
    edge_id: int
    e0: Dart
    e1: Dart
    e2: Dart
    e3: Dart

    @property
    def primal_darts(self):
        return self.e0, self.e2

    @property
    def dual_darts(self):
        return self.e1, self.e3


class QuadEdgeSubdivision:
    def __init__(self):
        self.edges = []
        self._next_id = 0

    def make_edge(self, origin=None, destination=None):
        e0, e1, e2, e3 = Dart(), Dart(), Dart(), Dart()
        e0.rot, e1.rot, e2.rot, e3.rot = e1, e2, e3, e0
        e0.primal = e2.primal = True
        e1.primal = e3.primal = False
        e0.onext, e1.onext, e2.onext, e3.onext = e0, e3, e2, e1
        e0.origin, e2.origin = origin, destination
        record = QuadEdge(self._next_id, e0, e1, e2, e3)
        self._next_id += 1
        self.edges.append(record)
        return e0

    @staticmethod
    def splice(a: Dart, b: Dart):
        """Exchange the two origin rings containing a and b."""
        alpha, beta = a.onext.rot, b.onext.rot
        a.onext, b.onext = b.onext, a.onext
        alpha.onext, beta.onext = beta.onext, alpha.onext

    def connect(self, a: Dart, b: Dart):
        """Create an edge from destination(a) to origin(b), joining left faces."""
        edge = self.make_edge(a.destination, b.origin)
        self.splice(edge, a.l_next)
        self.splice(edge.sym, b)
        return edge

    def delete_edge(self, edge: Dart):
        """Remove a primal edge from its origin rings (record retained as deleted)."""
        if not edge.primal:
            raise ValueError("delete_edge requires a primal dart")
        self.splice(edge, edge.o_prev)
        self.splice(edge.sym, edge.sym.o_prev)
        edge.origin = None
        edge.sym.origin = None
        edge.onext = edge
        edge.sym.onext = edge.sym

    def validate(self):
        """Check rotation cycles and onext closure for every retained edge record."""
        for record in self.edges:
            darts = (record.e0, record.e1, record.e2, record.e3)
            for i, dart in enumerate(darts):
                if dart.rot is not darts[(i+1) % 4]:
                    raise ValueError("broken four-dart rotation cycle")
                if dart.onext is None or dart.onext.rot is None:
                    raise ValueError("broken origin ring")
        return True

    def primal_edges(self):
        return tuple((e.e0.origin, e.e2.origin) for e in self.edges
                     if e.e0.origin is not None and e.e2.origin is not None)
