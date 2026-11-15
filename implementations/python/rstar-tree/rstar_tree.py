"""Mutable 2D R*-style tree. Forced reinsertion and deletion are omitted."""
from __future__ import annotations
from dataclasses import dataclass, field
from math import isfinite
from typing import Iterable

Bounds = tuple[float, float, float, float]

def _bounds(values: Iterable[float]) -> Bounds:
    b = tuple(float(v) for v in values)
    if len(b) != 4 or not all(isfinite(v) for v in b):
        raise ValueError("bounds must contain four finite values")
    if b[0] > b[2] or b[1] > b[3]:
        raise ValueError("minimum bounds must not exceed maximum bounds")
    return b

def _area(b): return (b[2]-b[0])*(b[3]-b[1])
def _margin(b): return 2*((b[2]-b[0])+(b[3]-b[1]))
def _union(a,b): return min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3])
def _overlap(a,b):
    return max(0.0,min(a[2],b[2])-max(a[0],b[0]))*max(0.0,min(a[3],b[3])-max(a[1],b[1]))

@dataclass
class _Node:
    leaf: bool
    children: list = field(default_factory=list)
    parent: "_Node | None" = None
    bounds: Bounds | None = None

@dataclass(frozen=True)
class _Entry:
    index: int
    bounds: Bounds

class RStarTree:
    """Incremental R*-style index for planar 2D axis-aligned boxes."""
    def __init__(self, max_entries: int = 8, min_fill: float = 0.4):
        if not isinstance(max_entries,int) or isinstance(max_entries,bool) or max_entries < 4:
            raise ValueError("max_entries must be an integer >= 4")
        if not isinstance(min_fill,(int,float)) or not 0.3 <= min_fill <= 0.5:
            raise ValueError("min_fill must be between 0.3 and 0.5")
        self.max_entries=max_entries
        self.min_entries=max(2,int(max_entries*min_fill+0.999999))
        if self.min_entries*2 > max_entries+1: raise ValueError("infeasible minimum fill")
        self.root=_Node(True)
        self._records=[]

    def _refresh(self,node):
        if not node.children:
            node.bounds=None
            return
        b=node.children[0].bounds
        for child in node.children[1:]: b=_union(b,child.bounds)
        node.bounds=b
        for child in node.children:
            if isinstance(child,_Node): child.parent=node

    def _choose_leaf(self,box):
        node=self.root
        while not node.leaf:
            scored=[]
            for child in node.children:
                cb=child.bounds
                enlarged=_union(cb,box)
                overlap_growth=sum(_overlap(enlarged,s.bounds)-_overlap(cb,s.bounds)
                                   for s in node.children if s is not child)
                scored.append((overlap_growth,_area(enlarged)-_area(cb),_area(cb),
                               len(child.children),child))
            node=min(scored,key=lambda x:x[:-1])[-1]
        return node

    def _split(self,node):
        items=node.children
        m,n=self.min_entries,len(items)
        best_axis,best_margin=0,float("inf")
        for axis in (0,1):
            total=0.0
            for lower in (True,False):
                ordered=sorted(items,key=lambda x:(x.bounds[axis] if lower else x.bounds[axis+2],
                                                    x.bounds[axis+2] if lower else x.bounds[axis]))
                for cut in range(m,n-m+1):
                    left,right=ordered[:cut],ordered[cut:]
                    lb,rb=left[0].bounds,right[0].bounds
                    for x in left[1:]: lb=_union(lb,x.bounds)
                    for x in right[1:]: rb=_union(rb,x.bounds)
                    total+=_margin(lb)+_margin(rb)
            if total<best_margin: best_axis,best_margin=axis,total
        choices=[]
        for lower in (True,False):
            ordered=sorted(items,key=lambda x:(x.bounds[best_axis] if lower else x.bounds[best_axis+2],
                                                x.bounds[best_axis+2] if lower else x.bounds[best_axis]))
            for cut in range(m,n-m+1):
                left,right=ordered[:cut],ordered[cut:]
                lb,rb=left[0].bounds,right[0].bounds
                for x in left[1:]: lb=_union(lb,x.bounds)
                for x in right[1:]: rb=_union(rb,x.bounds)
                choices.append((_overlap(lb,rb),_area(lb)+_area(rb),cut,left,right))
        _,_,_,left,right=min(choices,key=lambda x:x[:3])
        node.children=list(left); self._refresh(node)
        sibling=_Node(node.leaf,list(right),node.parent)
        self._refresh(sibling)
        return sibling

    def _adjust(self,node):
        while node is not None:
            self._refresh(node)
            if len(node.children)>self.max_entries:
                sibling=self._split(node)
                if node is self.root:
                    root=_Node(False,[node,sibling])
                    self.root=root; self._refresh(root)
                    return
                parent=node.parent
                parent.children.append(sibling)
                sibling.parent=parent
                node=parent
            else: node=node.parent

    def insert(self,bounds: Iterable[float]) -> int:
        box=_bounds(bounds)
        index=len(self._records)
        leaf=self._choose_leaf(box)
        leaf.children.append(_Entry(index,box))
        self._records.append(box)
        self._adjust(leaf)
        return index

    def query(self,bounds: Iterable[float]) -> list[int]:
        q=_bounds(bounds)
        if self.root.bounds is None: return []
        found=[]; stack=[self.root]
        while stack:
            node=stack.pop()
            b=node.bounds
            if b[2]<q[0] or q[2]<b[0] or b[3]<q[1] or q[3]<b[1]: continue
            for child in node.children:
                b=child.bounds
                if b[2]<q[0] or q[2]<b[0] or b[3]<q[1] or q[3]<b[1]: continue
                if isinstance(child,_Entry): found.append(child.index)
                else: stack.append(child)
        return sorted(found)

    def __len__(self): return len(self._records)
