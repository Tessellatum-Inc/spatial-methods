# Drainage-basin morphometry

Drainage-basin morphometry summarizes basin shape, relief and channel-network structure. Measures depend on basin-length and perimeter conventions and on channel extraction and ordering.

For area A, perimeter P, basin length Lb, relief H, total channel length Lt, total stream count Nt and stream counts Nu by order u:

- Form factor = A/Lb²; elongation ratio = 2√(A/π)/Lb.
- Circularity ratio = 4πA/P²; compactness coefficient = P/(2√(πA)).
- Drainage density = Lt/A; stream frequency = Nt/A; drainage texture = Nt/P.
- Bifurcation ratio = Nu/N(u+1); relief ratio = H/Lb; ruggedness number = (Lt/A)H.

The tested [package](../implementations/python/drainage-basin-morphometry/README.md) computes these from caller-supplied measurements. Report basin boundary, area/perimeter method, basin-length convention, DEM resolution, channel threshold, stream ordering and units. Drainage density is especially sensitive to network extraction scale.

Automatic basin delineation, channel extraction, ordering, uncertainty propagation and geomorphic interpretation are outside scope. See the [verification record](../catalog/verification/drainage-basin-morphometry.md).
