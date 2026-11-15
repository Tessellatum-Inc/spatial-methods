"""Local analytical hillshade from slope and downslope aspect."""
from __future__ import annotations
import numpy as np

def hillshade_from_slope_aspect(slope_degrees, aspect_degrees, *, sun_azimuth_degrees: float=315.0, sun_altitude_degrees: float=45.0) -> np.ndarray:
    """Return normalized local illumination in [0, 1].

    Azimuth is clockwise from north. Flat cells (zero slope) have no defined
    aspect and are assigned illumination equal to sin(sun altitude). This
    computes local illumination only; it does not cast terrain shadows.
    """
    slope=np.asarray(slope_degrees,dtype=float)
    aspect=np.asarray(aspect_degrees,dtype=float)
    if slope.shape!=aspect.shape:
        raise ValueError("slope and aspect arrays must have the same shape")
    if not np.isfinite([sun_azimuth_degrees,sun_altitude_degrees]).all():
        raise ValueError("sun angles must be finite")
    if not 0<=sun_altitude_degrees<=90:
        raise ValueError("sun altitude must be between 0 and 90 degrees")
    if ((slope[np.isfinite(slope)]<0)|(slope[np.isfinite(slope)]>90)).any():
        raise ValueError("finite slope values must be between 0 and 90 degrees")
    valid=np.isfinite(slope)
    flat=valid&(slope==0)
    angled=valid&np.isfinite(aspect)
    result=np.full(slope.shape,np.nan,dtype=float)
    altitude=np.radians(sun_altitude_degrees)
    azimuth=np.radians(sun_azimuth_degrees%360)
    sl=np.radians(slope[angled])
    asp=np.radians(aspect[angled]%360)
    illumination=np.sin(altitude)*np.cos(sl)+np.cos(altitude)*np.sin(sl)*np.cos(azimuth-asp)
    result[angled]=np.clip(illumination,0.0,1.0)
    result[flat]=np.sin(altitude)
    return result



def multidirectional_hillshade(
    slope_degrees,
    aspect_degrees,
    *,
    sun_azimuths=(225.0, 270.0, 315.0, 360.0),
    sun_altitude_degrees: float = 45.0,
) -> np.ndarray:
    """Average local hillshade from several azimuths at one altitude.

    The default four-azimuth composite reduces the directional bias of a
    single light source. It averages equally weighted normalized local
    illumination; it does not model cast shadows or diffuse radiance.
    """
    try:
        azimuths = np.asarray(tuple(sun_azimuths), dtype=float)
    except (TypeError, ValueError):
        raise ValueError("sun_azimuths must be a non-empty sequence of finite angles") from None
    if azimuths.ndim != 1 or azimuths.size == 0 or not np.isfinite(azimuths).all():
        raise ValueError("sun_azimuths must be a non-empty sequence of finite angles")
    slope = np.asarray(slope_degrees, dtype=float)
    aspect = np.asarray(aspect_degrees, dtype=float)
    if slope.shape != aspect.shape:
        raise ValueError("slope and aspect arrays must have the same shape")
    shades = [
        hillshade_from_slope_aspect(
            slope, aspect,
            sun_azimuth_degrees=float(azimuth),
            sun_altitude_degrees=sun_altitude_degrees,
        )
        for azimuth in azimuths
    ]
    stack = np.stack(shades, axis=0)
    valid_count = np.isfinite(stack).sum(axis=0)
    total = np.nansum(stack, axis=0)
    result = np.full(slope.shape, np.nan, dtype=float)
    np.divide(total, valid_count, out=result, where=valid_count > 0)
    return result
