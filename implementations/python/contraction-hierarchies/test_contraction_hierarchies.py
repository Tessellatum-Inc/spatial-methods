import heapq
import math
import random

import pytest

from contraction_hierarchies import ContractionHierarchy


def dijkstra(n, edges, source, target):
    adjacency=[[] for _ in range(n)]
    for u,v,w in edges:
        adjacency[u].append((v,float(w)))
    distance=[math.inf]*n
    distance[source]=0.0
    queue=[(0.0,source)]
    while queue:
        d,u=heapq.heappop(queue)
        if d!=distance[u]:
            continue
        if u==target:
            return d
        for v,w in adjacency[u]:
            candidate=d+w
            if candidate<distance[v]:
                distance[v]=candidate
                heapq.heappush(queue,(candidate,v))
    return math.inf


def path_weight(path, edges):
    total=0.0
    for u,v in zip(path,path[1:]):
        total+=min(w for a,b,w in edges if a==u and b==v)
    return total


def test_contraction_adds_and_unpacks_required_shortcut():
    edges=[(0,1,1),(1,2,1),(0,2,5)]
    hierarchy=ContractionHierarchy(3,edges,order=[1,0,2])
    result=hierarchy.query(0,2)
    assert result["distance"]==pytest.approx(2)
    assert result["path"]==[0,1,2]
    assert len(result["edge_ids"])==2
    assert hierarchy.shortcut_count==0


def test_witness_search_suppresses_unnecessary_shortcut():
    edges=[(0,1,1),(1,2,1),(0,2,1)]
    hierarchy=ContractionHierarchy(3,edges,order=[1,0,2])
    assert hierarchy.query(0,2)["distance"]==pytest.approx(1)
    assert hierarchy.shortcut_count==0


def test_bidirectional_upward_queries_match_dijkstra_on_seeded_random_graphs():
    rng=random.Random(20261117)
    for _ in range(35):
        n=rng.randint(2,9)
        edges=[]
        for u in range(n):
            for v in range(n):
                if u!=v and rng.random()<.22:
                    edges.append((u,v,rng.randint(0,25)))
        order=list(range(n))
        rng.shuffle(order)
        hierarchy=ContractionHierarchy(n,edges,order=order)
        for source in range(n):
            for target in range(n):
                expected=dijkstra(n,edges,source,target)
                result=hierarchy.query(source,target)
                assert result["distance"]==pytest.approx(expected)
                if math.isfinite(expected):
                    assert result["path"][0]==source and result["path"][-1]==target
                    assert path_weight(result["path"],edges)==pytest.approx(expected)
                else:
                    assert result["path"]==[]


def test_parallel_edges_zero_weights_and_same_node_queries():
    edges=[(0,1,5),(0,1,2),(1,2,0),(2,3,3)]
    hierarchy=ContractionHierarchy(4,edges,order=[1,2,0,3])
    assert hierarchy.query(0,3)["distance"]==pytest.approx(5)
    assert hierarchy.query(2,2)=={
        "distance":0.0,"path":[2],"edge_ids":[],"meeting_node":2}
    assert hierarchy.query(0,3,return_path=False)["path"]==[]


def test_unreachable_nodes_and_empty_graph():
    hierarchy=ContractionHierarchy(3,[])
    assert math.isinf(hierarchy.query(0,2)["distance"])
    assert hierarchy.query(0,2)["path"]==[]


@pytest.mark.parametrize("args,kwargs",[
    ((0,[]),{}),((2,[(0,2,1)]),{}),((2,[(0,1,-1)]),{}),
    ((2,[(0,1,float("nan"))]),{}),((2,[(0,0,1)]),{}),
    ((3,[(0,1,1)]),{"order":[0,0,2]}),
])
def test_invalid_preprocessing_inputs_are_rejected(args,kwargs):
    with pytest.raises(ValueError):
        ContractionHierarchy(*args,**kwargs)


def test_invalid_query_nodes_are_rejected():
    hierarchy=ContractionHierarchy(2,[(0,1,1)])
    with pytest.raises(ValueError):
        hierarchy.query(-1,1)
