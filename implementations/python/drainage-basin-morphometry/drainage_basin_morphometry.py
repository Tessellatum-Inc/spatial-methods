"""Classic drainage-basin shape and network ratios from supplied measurements."""
import math

def drainage_basin_morphometry(*, area, perimeter, basin_length, relief, stream_lengths, stream_counts):
    """All linear measures share units; area uses their square. Counts keyed by stream order."""
    vals=(area,perimeter,basin_length,relief)
    if any(not math.isfinite(float(v)) for v in vals): raise ValueError("basin measures must be finite")
    area,perimeter,basin_length,relief=map(float,vals)
    if area<=0 or perimeter<=0 or basin_length<=0 or relief<0: raise ValueError("invalid basin geometry or relief")
    lengths=[float(v) for v in stream_lengths]
    if any(not math.isfinite(v) or v<0 for v in lengths): raise ValueError("stream lengths must be finite and non-negative")
    counts={}
    for order,count in stream_counts.items():
        if isinstance(order,bool) or not isinstance(order,int) or order<1: raise ValueError("stream orders must be positive integers")
        if isinstance(count,bool) or not isinstance(count,int) or count<0: raise ValueError("stream counts must be non-negative integers")
        counts[order]=count
    total_length=math.fsum(lengths); total_count=sum(counts.values()); density=total_length/area
    return {"area":area,"perimeter":perimeter,"basin_length":basin_length,"relief":relief,
      "total_stream_length":total_length,"total_stream_count":total_count,
      "form_factor":area/(basin_length**2),"elongation_ratio":2*math.sqrt(area/math.pi)/basin_length,
      "circularity_ratio":4*math.pi*area/(perimeter**2),
      "compactness_coefficient":perimeter/(2*math.sqrt(math.pi*area)),
      "drainage_density":density,"stream_frequency":total_count/area,
      "drainage_texture":total_count/perimeter,"relief_ratio":relief/basin_length,
      "ruggedness_number":density*relief,
      "bifurcation_ratios":{u:counts[u]/counts[u+1] for u in sorted(counts) if u+1 in counts and counts[u+1]>0}}
