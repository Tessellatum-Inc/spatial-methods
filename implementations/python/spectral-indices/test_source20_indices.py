import numpy as np
import pytest
from spectral_indices import (ari, arvi, bsi, cai, ci_green, ci_rededge, cri1, cri2,
    gci, gndvi, kndvi, msavi, mtci, ndii, ndti, nirv, nmdi, osavi, pri, psri,
    reip, sipi, sti, tcari, wdrvi)

def test_green_and_atmospheric_vegetation_indices():
    n,r,g,b=.6,.2,.3,.1
    assert gndvi(n,g)==pytest.approx((n-g)/(n+g))
    assert arvi(n,r,b)==pytest.approx((n-(2*r-b))/(n+(2*r-b)))
    assert gci(n,g)==pytest.approx(n/g-1)
    assert ci_green(n,g)==pytest.approx(gci(n,g))
    assert ci_rededge(n,.4)==pytest.approx(n/.4-1)

def test_soil_adjusted_and_dynamic_range_indices():
    n,r=.6,.2
    assert msavi(n,r)==pytest.approx((2*n+1-np.sqrt((2*n+1)**2-8*(n-r)))/2)
    assert osavi(n,r)==pytest.approx(1.16*(n-r)/(n+r+.16))
    assert wdrvi(n,r,alpha=.2)==pytest.approx((.2*n-r)/(.2*n+r))

def test_nirv_and_kernel_ndvi():
    n,r=.6,.2; nd=(n-r)/(n+r)
    assert nirv(n,r)==pytest.approx(nd*n)
    assert kndvi(n,r)==pytest.approx(np.tanh(nd**2))

def test_red_edge_indices():
    r,re1,re2,n780=.2,.4,.5,.78
    assert mtci(r,re1,re2)==pytest.approx((re2-re1)/(re1-r))
    assert reip(r,re1,re2,n780)==pytest.approx(700+40*((r+n780)/2-re1)/(re2-re1))
    assert tcari(r,.3,re1)==pytest.approx(3*((re1-r)-.2*(re1-.3)*(re1/r)))

def test_pigment_and_photochemical_indices():
    r,g,re,b=.2,.3,.4,.1
    assert psri(r,g,re)==pytest.approx((r-g)/re)
    assert ari(g,re)==pytest.approx(1/g-1/re)
    assert cri1(b,g)==pytest.approx(1/b-1/g)
    assert cri2(b,re)==pytest.approx(1/b-1/re)
    assert sipi(.6,b,r)==pytest.approx((.6-b)/(.6-r))
    assert pri(.4,.3)==pytest.approx((.4-.3)/(.4+.3))

def test_water_tillage_and_bare_soil_indices():
    n,s1,s2=.6,.15,.08; b,r=.1,.2
    assert ndii(n,s1)==pytest.approx((n-s1)/(n+s1))
    assert nmdi(n,s1,s2)==pytest.approx((n-(s1-s2))/(n+(s1-s2)))
    assert bsi(b,r,n,s1)==pytest.approx(((s1+r)-(n+b))/((s1+r)+(n+b)))
    assert ndti(s1,s2)==pytest.approx((s1-s2)/(s1+s2))
    assert sti(s1,s2)==pytest.approx(s1/s2)
    assert cai(2.,3.,4.)==pytest.approx(0.)

def test_mask_and_nodata_contract():
    n=np.array([.6,.5,-9999.,np.nan]);r=np.array([.2,.1,-9999.,.1])
    mask=np.array([True,False,True,True])
    for fn in (gndvi,msavi,osavi,wdrvi,nirv,kndvi):
        out=fn(n,r,nodata=-9999.,valid_mask=mask)
        assert np.isfinite(out[0]); assert np.isnan(out[1:]).all()

def test_undefined_ratios_return_nan():
    assert np.isnan(gndvi(1.,-1.))
    assert np.isnan(gci(1.,0.))
    assert np.isnan(mtci(.2,.2,.5))
    assert np.isnan(sipi(.5,.1,.5))
    assert np.isnan(sti(.5,0.))

def test_shape_mask_and_parameter_validation():
    with pytest.raises(ValueError): arvi(np.ones(2),np.ones(3),np.ones(2))
    with pytest.raises(TypeError): nmdi(np.ones(2),np.ones(2),np.ones(2),valid_mask=np.ones(2,dtype=int))
    with pytest.raises(ValueError): arvi(.6,.2,.1,gamma=-1)
    with pytest.raises(ValueError): wdrvi(.6,.2,alpha=0)
