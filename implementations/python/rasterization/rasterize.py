"""Small-grid rasterization algorithms with explicit cell contracts."""
from __future__ import annotations
from math import floor, isfinite

def _point(p):
    if len(p) != 2:
        raise ValueError("points must be (x, y) pairs")
    x,y=float(p[0]),float(p[1])
    if not isfinite(x) or not isfinite(y):
        raise ValueError("coordinates must be finite")
    return x,y

def _round_pixel(v):
    return floor(v + 0.5)

def dda_line(start, end):
    """DDA thin line; endpoints are pixel-centre coordinates, ties round upward."""
    x0,y0=_point(start); x1,y1=_point(end)
    dx,dy=x1-x0,y1-y0
    steps=int(max(abs(dx),abs(dy)))
    if steps==0:
        return [( _round_pixel(x0), _round_pixel(y0) )]
    cells=[]
    for k in range(steps+1):
        t=k/steps
        cell=(_round_pixel(x0+t*dx),_round_pixel(y0+t*dy))
        if not cells or cell!=cells[-1]:
            cells.append(cell)
    return cells

def bresenham_line(start, end):
    """Integer Bresenham line for all octants; endpoints are rounded pixel centres."""
    x0,y0=map(_round_pixel,_point(start)); x1,y1=map(_round_pixel,_point(end))
    dx=abs(x1-x0); sx=1 if x0<x1 else -1
    dy=-abs(y1-y0); sy=1 if y0<y1 else -1
    err=dx+dy; out=[]
    while True:
        out.append((x0,y0))
        if x0==x1 and y0==y1: break
        e2=2*err
        if e2>=dy: err+=dy; x0+=sx
        if e2<=dx: err+=dx; y0+=sy
    return out

def wu_line(start, end):
    """Xiaolin Wu antialiased line as (column, row, coverage) tuples."""
    x0,y0=_point(start); x1,y1=_point(end)
    steep=abs(y1-y0)>abs(x1-x0)
    if steep: x0,y0=y0,x0; x1,y1=y1,x1
    if x0>x1: x0,x1=x1,x0; y0,y1=y1,y0
    dx=x1-x0; dy=y1-y0
    if abs(dx)<1e-15:
        return [( _round_pixel(y0), _round_pixel(x0), 1.0 )]
    gradient=dy/dx
    def ipart(x): return floor(x)
    def fpart(x): return x-floor(x)
    def rfpart(x): return 1-fpart(x)
    result=[]
    xend=_round_pixel(x0); yend=y0+gradient*(xend-x0); xgap=rfpart(x0+0.5)
    xpxl1=xend; ypxl1=ipart(yend)
    result.extend([(ypxl1,xpxl1,rfpart(yend)*xgap),(ypxl1+1,xpxl1,fpart(yend)*xgap)])
    intery=yend+gradient
    xend=_round_pixel(x1); yend=y1+gradient*(xend-x1); xgap=fpart(x1+0.5)
    xpxl2=xend; ypxl2=ipart(yend)
    for x in range(xpxl1+1,xpxl2):
        y=ipart(intery)
        result.extend([(y,x,rfpart(intery)),(y+1,x,fpart(intery))])
        intery+=gradient
    result.extend([(ypxl2,xpxl2,rfpart(yend)*xgap),(ypxl2+1,xpxl2,fpart(yend)*xgap)])
    if steep: result=[(x,y,w) for y,x,w in result]
    return [(x,y,max(0.0,min(1.0,w))) for x,y,w in result if w>0]

def _segment_intersects_rect(x0,y0,x1,y1,xmin,ymin,xmax,ymax):
    """Closed Liang–Barsky segment/rectangle intersection."""
    dx,dy=x1-x0,y1-y0; t0,t1=0.0,1.0
    for p,q in [(-dx,x0-xmin),(dx,xmax-x0),(-dy,y0-ymin),(dy,ymax-y0)]:
        if abs(p)<1e-15:
            if q<0: return False
        else:
            t=q/p
            if p<0:
                if t>t1: return False
                t0=max(t0,t)
            else:
                if t<t0: return False
                t1=min(t1,t)
    return t0<=t1

def supercover_line(start, end):
    """Every closed unit cell touched by a segment in grid-corner coordinates.

    Cells are (column,row); edge- and corner-only touches are included. This
    conservative contract can emit multiple cells at exact grid-corner crossings.
    """
    x0,y0=_point(start); x1,y1=_point(end)
    xmin, xmax = min(x0,x1), max(x0,x1)
    ymin, ymax = min(y0,y1), max(y0,y1)
    c0=floor(xmin) - (1 if xmin == floor(xmin) else 0); c1=floor(xmax)
    r0=floor(ymin) - (1 if ymin == floor(ymin) else 0); r1=floor(ymax)
    cells=[]
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if _segment_intersects_rect(x0,y0,x1,y1,c,r,c+1,r+1):
                cells.append((c,r))
    return cells

def scanline_fill(polygon, rows, cols):
    """Even–odd polygon fill by cell-centre sampling; returns bool[row][col]."""
    pts=[_point(p) for p in polygon]
    if len(pts)<3:
        raise ValueError("polygon requires at least three vertices")
    if isinstance(rows,bool) or not isinstance(rows,int) or rows<1 or isinstance(cols,bool) or not isinstance(cols,int) or cols<1:
        raise ValueError("rows and cols must be positive integers")
    grid=[[False]*cols for _ in range(rows)]
    for r in range(rows):
        y=r+0.5
        intersections=[]
        for i,(x0,y0) in enumerate(pts):
            x1,y1=pts[(i+1)%len(pts)]
            if (y0<=y<y1) or (y1<=y<y0):
                intersections.append(x0+(y-y0)*(x1-x0)/(y1-y0))
        intersections.sort()
        for k in range(0,len(intersections)-1,2):
            left,right=intersections[k],intersections[k+1]
            for c in range(cols):
                x=c+0.5
                if left<=x<right:
                    grid[r][c]=True
    return grid
