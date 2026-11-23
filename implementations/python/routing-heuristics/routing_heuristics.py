"""Small-instance Euclidean TSP/VRP heuristics with explicit assumptions."""
from __future__ import annotations

from math import hypot, isfinite
from dataclasses import dataclass
from typing import Iterable, Sequence

Point = tuple[float, float]


def _points(values: Iterable[Sequence[float]]) -> list[Point]:
    out=[]
    for value in values:
        try: p=tuple(float(v) for v in value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("each point must contain two finite coordinates") from exc
        if len(p)!=2 or not all(isfinite(v) for v in p):
            raise ValueError("each point must contain two finite coordinates")
        out.append((p[0],p[1]))
    return out


def route_length(route: Sequence[int], points: Sequence[Point], *, closed: bool=True) -> float:
    """Euclidean route length for integer point indices."""
    if len(route)<2: return 0.0
    pairs=list(zip(route,route[1:]))
    if closed: pairs.append((route[-1],route[0]))
    return sum(hypot(points[a][0]-points[b][0],points[a][1]-points[b][1]) for a,b in pairs)


def two_opt(points: Iterable[Sequence[float]], route: Sequence[int] | None=None,
            *, max_passes: int=100) -> list[int]:
    """Improve a closed Euclidean TSP tour using deterministic 2-opt reversals.

    The first point is fixed to remove rotational symmetry. The initial tour
    defaults to input order. Strictly improving moves only; ties retain order.
    This is a local-search heuristic, not an optimal TSP solver.
    """
    pts=_points(points); n=len(pts)
    if isinstance(max_passes,bool) or not isinstance(max_passes,int) or max_passes<1:
        raise ValueError("max_passes must be a positive integer")
    tour=list(range(n)) if route is None else list(route)
    if (len(tour)!=n or any(isinstance(i,bool) or not isinstance(i,int) for i in tour)
            or set(tour)!=set(range(n))):
        raise ValueError("route must be a permutation of all integer point indices")
    if n<4: return tour
    if tour[0]!=0:
        k=tour.index(0); tour=tour[k:]+tour[:k]
    for _ in range(max_passes):
        improved=False
        for i in range(1,n-1):
            a,b=tour[i-1],tour[i]
            for j in range(i+1,n):
                c,d=tour[j],tour[(j+1)%n]
                old=hypot(pts[a][0]-pts[b][0],pts[a][1]-pts[b][1])+hypot(pts[c][0]-pts[d][0],pts[c][1]-pts[d][1])
                new=hypot(pts[a][0]-pts[c][0],pts[a][1]-pts[c][1])+hypot(pts[b][0]-pts[d][0],pts[b][1]-pts[d][1])
                if new < old-1e-12:
                    tour[i:j+1]=reversed(tour[i:j+1]); improved=True
        if not improved: break
    return tour


def clarke_wright_cvrp(points: Iterable[Sequence[float]], demands: Sequence[float],
                       capacity: float, *, depot: int=0) -> list[list[int]]:
    """Construct capacity-feasible depot routes using parallel savings.

    Returns routes as [depot, customer, ..., depot]. Every customer is served
    once. Demands are indivisible and non-negative. This is the classical
    parallel Clarke-Wright savings heuristic for symmetric Euclidean costs;
    it does not solve VRPTW, split deliveries, fleet-size limits or pickup-
    delivery precedence.
    """
    pts=_points(points); n=len(pts)
    if n==0: raise ValueError("at least a depot point is required")
    if isinstance(depot,bool) or not isinstance(depot,int) or not 0<=depot<n:
        raise ValueError("depot must be a valid point index")
    if len(demands)!=n: raise ValueError("demands must have one value per point")
    ds=[]
    for d in demands:
        try: v=float(d)
        except (TypeError,ValueError,OverflowError) as exc: raise ValueError("demands must be finite and non-negative") from exc
        if not isfinite(v) or v<0: raise ValueError("demands must be finite and non-negative")
        ds.append(v)
    try: cap=float(capacity)
    except (TypeError,ValueError,OverflowError) as exc: raise ValueError("capacity must be positive and finite") from exc
    if not isfinite(cap) or cap<=0: raise ValueError("capacity must be positive and finite")
    if ds[depot]!=0: raise ValueError("depot demand must be zero")
    customers=[i for i in range(n) if i!=depot]
    if any(ds[i]>cap for i in customers): raise ValueError("a customer demand exceeds vehicle capacity")
    routes={i:[i] for i in customers}; loads={i:ds[i] for i in customers}
    owner={i:i for i in customers}
    savings=[]
    for ix,i in enumerate(customers):
        for j in customers[ix+1:]:
            dij=hypot(pts[i][0]-pts[j][0],pts[i][1]-pts[j][1])
            di0=hypot(pts[i][0]-pts[depot][0],pts[i][1]-pts[depot][1])
            dj0=hypot(pts[j][0]-pts[depot][0],pts[j][1]-pts[depot][1])
            savings.append((di0+dj0-dij,i,j))
    savings.sort(key=lambda x:(-x[0],x[1],x[2]))
    for _,i,j in savings:
        ri,rj=owner[i],owner[j]
        if ri==rj or loads[ri]+loads[rj]>cap: continue
        a,b=routes[ri],routes[rj]
        if i not in (a[0],a[-1]) or j not in (b[0],b[-1]): continue
        if i==a[0]: a=list(reversed(a))
        if j==b[-1]: b=list(reversed(b))
        merged=a+b
        routes[ri]=merged; loads[ri]+=loads[rj]
        for customer in b: owner[customer]=ri
        del routes[rj]; del loads[rj]
    return [[depot,*routes[k],depot] for k in sorted(routes)]


def validate_cvrp_routes(routes: Sequence[Sequence[int]], demands: Sequence[float],
                         capacity: float, *, depot: int=0) -> bool:
    """Return whether routes serve every non-depot index once within capacity."""
    n=len(demands); seen=[]
    try:
        for route in routes:
            if len(route)<3 or route[0]!=depot or route[-1]!=depot: return False
            customers=list(route[1:-1])
            if depot in customers or any(not isinstance(i,int) or not 0<=i<n for i in customers): return False
            if sum(float(demands[i]) for i in customers)>capacity+1e-12: return False
            seen.extend(customers)
        return sorted(seen)==[i for i in range(n) if i!=depot]
    except (TypeError,ValueError,IndexError):
        return False


@dataclass(frozen=True)
class VRPTWStop:
    """Arrival, service-start and departure times for one route stop."""

    node: int
    arrival: float
    service_start: float
    departure: float


@dataclass(frozen=True)
class VRPTWRoute:
    """One depot-closed vehicle route and its feasible schedule."""

    nodes: tuple[int, ...]
    stops: tuple[VRPTWStop, ...]
    load: float
    distance: float


@dataclass(frozen=True)
class VRPTWResult:
    """Constructed routes plus customers that the heuristic could not serve."""

    routes: tuple[VRPTWRoute, ...]
    unserved: tuple[int, ...]


def greedy_vrptw(
    points: Iterable[Sequence[float]],
    demands: Sequence[float],
    time_windows: Sequence[Sequence[float]],
    capacity: float,
    service_times: Sequence[float] | None = None,
    *,
    depot: int = 0,
    vehicle_limit: int | None = None,
    start_time: float | None = None,
) -> VRPTWResult:
    """Build feasible Euclidean VRPTW routes by deterministic greedy insertion.

    At each stop, choose the feasible unserved customer with the smallest
    incremental closed-route distance. Waiting is allowed. A candidate is
    feasible only if capacity, its service-start window and return to the
    depot by the depot's closing time are all satisfied.

    This is a constructive heuristic, not an exact VRPTW solver. It can leave
    customers unserved even when a different ordering could serve them.
    """
    pts = _points(points)
    n = len(pts)
    if n == 0:
        raise ValueError("at least a depot point is required")
    if isinstance(depot, bool) or not isinstance(depot, int) or not 0 <= depot < n:
        raise ValueError("depot must be a valid point index")
    if len(demands) != n or len(time_windows) != n:
        raise ValueError("demands and time_windows must have one value per point")

    ds = []
    for demand in demands:
        try:
            value = float(demand)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("demands must be finite and non-negative") from exc
        if not isfinite(value) or value < 0:
            raise ValueError("demands must be finite and non-negative")
        ds.append(value)

    try:
        cap = float(capacity)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("capacity must be positive and finite") from exc
    if not isfinite(cap) or cap <= 0:
        raise ValueError("capacity must be positive and finite")
    if ds[depot] != 0:
        raise ValueError("depot demand must be zero")
    if any(ds[i] > cap for i in range(n) if i != depot):
        raise ValueError("a customer demand exceeds vehicle capacity")

    windows = []
    for window in time_windows:
        try:
            pair = tuple(float(value) for value in window)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("each time window must contain two finite values") from exc
        if len(pair) != 2 or not all(isfinite(value) for value in pair) or pair[0] > pair[1]:
            raise ValueError("each time window must be finite and ordered")
        windows.append((pair[0], pair[1]))

    if service_times is None:
        services = [0.0] * n
    else:
        if len(service_times) != n:
            raise ValueError("service_times must have one value per point")
        services = []
        for duration in service_times:
            try:
                value = float(duration)
            except (TypeError, ValueError, OverflowError) as exc:
                raise ValueError("service times must be finite and non-negative") from exc
            if not isfinite(value) or value < 0:
                raise ValueError("service times must be finite and non-negative")
            services.append(value)

    if vehicle_limit is not None and (
        isinstance(vehicle_limit, bool)
        or not isinstance(vehicle_limit, int)
        or vehicle_limit < 1
    ):
        raise ValueError("vehicle_limit must be a positive integer or None")
    if start_time is None:
        dispatch = windows[depot][0]
    else:
        try:
            dispatch = float(start_time)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("start_time must be finite") from exc
        if not isfinite(dispatch):
            raise ValueError("start_time must be finite")
        dispatch = max(dispatch, windows[depot][0])
    if dispatch > windows[depot][1]:
        raise ValueError("start_time is after the depot closing time")

    def distance(a: int, b: int) -> float:
        return hypot(pts[a][0] - pts[b][0], pts[a][1] - pts[b][1])

    unserved = set(i for i in range(n) if i != depot)
    routes = []
    while unserved and (vehicle_limit is None or len(routes) < vehicle_limit):
        current = depot
        departure = dispatch
        load = 0.0
        route_nodes = [depot]
        stops = [VRPTWStop(depot, dispatch, dispatch, dispatch)]
        route_distance = 0.0

        while True:
            feasible = []
            for customer in sorted(unserved):
                if load + ds[customer] > cap + 1e-12:
                    continue
                leg = distance(current, customer)
                arrival = departure + leg
                service_start = max(arrival, windows[customer][0])
                if service_start > windows[customer][1]:
                    continue
                next_departure = service_start + services[customer]
                return_time = next_departure + distance(customer, depot)
                if return_time > windows[depot][1]:
                    continue
                detour = leg + distance(customer, depot) - distance(current, depot)
                feasible.append((detour, customer, arrival, service_start, next_departure, leg))

            if not feasible:
                break
            _, chosen, arrival, service_start, next_departure, leg = min(
                feasible, key=lambda item: (item[0], item[1])
            )
            route_distance += leg
            route_nodes.append(chosen)
            stops.append(VRPTWStop(chosen, arrival, service_start, next_departure))
            load += ds[chosen]
            departure = next_departure
            current = chosen
            unserved.remove(chosen)

        if len(route_nodes) == 1:
            break

        return_leg = distance(current, depot)
        return_time = departure + return_leg
        route_distance += return_leg
        route_nodes.append(depot)
        stops.append(VRPTWStop(depot, return_time, return_time, return_time))
        routes.append(
            VRPTWRoute(tuple(route_nodes), tuple(stops), load, route_distance)
        )

    return VRPTWResult(tuple(routes), tuple(sorted(unserved)))
