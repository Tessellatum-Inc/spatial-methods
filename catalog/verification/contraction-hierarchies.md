# Source verification — contraction hierarchies

## Identity and bibliography
- Geisberger, R., Sanders, P., Schultes, D., & Delling, D. (2008). “Contraction Hierarchies: Faster and Simpler Hierarchical Routing in Road Networks.” *Experimental Algorithms*, LNCS 5038, 319–333. DOI 10.1007/978-3-540-68552-4_24.
- Geisberger, R., Sanders, P., Schultes, D., & Vetter, C. (2012). “Exact Routing in Large Road Networks Using Contraction Hierarchies.” *Transportation Science*, 46(3), 388–404. DOI 10.1287/trsc.1110.0401.

## Technical claims
- Preprocessing contracts vertices in an importance order and adds shortcuts when a witness path of no greater cost does not avoid the contracted vertex.
- Queries use bidirectional upward search and shortcut unpacking.

## Implementation and tests
- Static directed nonnegative graph; unrestricted Dijkstra witness searches; supplied or static-degree contraction order.
- Independent all-pairs Dijkstra oracle on seeded random directed graphs, plus shortcut/witness, path reconstruction, zero/parallel edge and invalid-input tests.

## Limits and rights
No advanced ordering, dynamic customization, time-dependent/turn-cost routing, witness limits or large-network performance claim. Original code and explanatory text; bibliographic metadata only.
