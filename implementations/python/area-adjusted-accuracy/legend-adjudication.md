# Legend adjudication: Fiji reference labels and ESA WorldCover 2021 v200

**Status:** Documentary legend review completed; point-level image adjudication not yet performed. This note explains where the two class systems align, where they do not, and what the existing error transitions can and cannot mean.

## Why the comparison needs a legend review

The Fiji reference sample and WorldCover both describe 2021, but their class definitions are not interchangeable. The Fiji test dataset uses eight labels: water, mangrove, bare earth/rock, urban/impervious, agriculture, grassland, shrubland and tree. The test-dataset page says its reference points were manually labelled from 2021 annual-median Sentinel-2 and Planet NICFI RGB composites and high-resolution Google Satellite basemaps. The Fiji project’s related land-cover-label documentation gives operational descriptions for agriculture, grassland, scrubland and trees. Those descriptions are useful evidence about the project’s label ontology, but the test-sample documentation does not reproduce a full point-interpreter protocol; therefore they should not be treated as a definitive adjudication rulebook for every one of the 834 points.

WorldCover 2021 v200 uses the FAO Land Cover Classification System and 11 classes. Its classes use cover thresholds, vegetation form and land-use rules that differ from the Fiji project’s visual height/structure descriptions.

## Definitions side by side

| Theme | Fiji project label description | WorldCover 2021 v200 definition | Consequence for this comparison |
|---|---|---|---|
| Tree / tree cover | Trees are vegetation greater than head height forming a clear canopy. | Tree cover is an area dominated by trees with at least 10% tree cover. Shrubs or herbs can occur beneath the canopy; plantations, including oil palm, are included. | A visible-canopy/height rule and a 10% cover rule are not equivalent. WorldCover may call a mixed or open woody pixel tree cover where the Fiji visual label is shrubland or grassland. |
| Shrubland / scrubland | Vegetation below head height, not forming a closed canopy, with clearly visible bush, shrub or woody structure. | Natural shrubs with at least 10% cover; shrubs are woody perennial plants with persistent woody stems, no defined main stem and height below 5 m. Scattered trees are allowed if tree cover is below 10%; herbs may occur at any density. | Both systems recognise woody shrubs, but the thresholds and decision cues differ. Fiji's relative height and canopy description cannot be translated directly into WorldCover's shrub cover and plant-form rule. |
| Grassland | Low vegetation (for example, below knee height) without a bush, shrub or woody structure. | Natural herbaceous plants with at least 10% cover; trees and shrubs may be present if their cover is below 10%. Pastures are included, as are some uncultivated cropland areas without a harvest/bare-soil period in the reference year. | The Fiji description is a visual structure/height rule; WorldCover allows a small woody component and explicitly includes pasture. Borderline savanna, open woodland and grazing landscapes may be labelled differently. |
| Agriculture / cropland | Cropping or livestock-management activity visible in high-resolution imagery; recently fallow land remains agriculture where evidence of cropping or grazing is visible. | Annual cropland that is sown/planted and harvestable at least once within 12 months after planting. Perennial woody crops are assigned to tree or shrub classes; greenhouses are built-up. | This is a material ontology mismatch. Fiji's class includes evidence of livestock management and recently fallow land; WorldCover's cropland is annual-crop focused and assigns pasture and perennial woody crops elsewhere. |
| Herbaceous wetland | No separate wetland class in the Fiji eight-class test legend. | Natural herbaceous vegetation with at least 10% cover that is permanently or regularly flooded; excludes swamp forests (tree cover), mangroves and unvegetated sediment. | A WorldCover wetland pixel has no direct Fiji class counterpart. Counting it as disagreement is mathematically consistent with the strict eight-class matrix, but does not by itself establish a thematic error. |

**Source boundary:** the Fiji definitions above come from the broader Fiji Land Use Land Cover Labels project page, not a separately published detailed interpreter manual for the 834-point test sample. The test dataset itself confirms the eight class names, the manual visual interpretation process and the 2021 image sources. The distinction matters: this review identifies a plausible schema mismatch; it does not retroactively prove how every sample point was labelled.

## Re-reading the dominant transitions

### 1. WorldCover tree → Fiji reference shrubland

The 89-point transition contributes an estimated 10.13 percentage points of error under the strict crosswalk. It is the largest single transition, but the definitions show that it cannot yet be called 89 straightforward classifier mistakes.

Potential mechanisms include:
- a pixel with at least 10% tree cover meeting WorldCover's tree-cover rule while the Fiji interpreter judged the visible vegetation to be below head height or not a clear tree canopy;
- mixed woody vegetation where shrub and tree cover coexist;
- different interpretation of open woodland, woody savanna or shrub-dominated vegetation;
- differences in the spatial support of a point label and a 10 m pixel.

These are testable hypotheses, not findings. A per-point image review is required to decide which, if any, applies.

### 2. WorldCover tree/grassland → Fiji reference agriculture

Of 69 reference-agriculture points, WorldCover predicts cropland at only two. The two largest observed transitions are grassland (38 points; 3.13 weighted percentage points) and tree cover (25 points; 2.13 weighted percentage points).

The class definitions provide a particularly strong reason not to interpret all of this as ordinary classification failure:
- Fiji's agriculture label includes visible evidence of livestock management and can include recently fallow land.
- WorldCover explicitly includes pasture in grassland.
- WorldCover assigns perennial woody crops to tree or shrub classes rather than annual cropland.

Thus, a portion of the apparent omission may be a land-use-versus-land-cover distinction: the Fiji label can encode agricultural use or management evidence, while WorldCover classifies the observed physical cover. The existing sample results do not tell us how many of the 38 grassland or 25 tree transitions are pasture, fallow, annual crop, plantation or another cover type.

### 3. WorldCover herbaceous wetland → Fiji reference tree

Seven points contribute 1.75 weighted percentage points to this transition. WorldCover's wetland definition explicitly excludes swamp forests, which it places in tree cover, and mangroves, which have their own class. Fiji has no wetland class in its eight-class legend. The reference-tree labels may therefore represent woody wetland or swamp-forest vegetation, or they may reflect interpretation differences. Without point imagery and ancillary hydrological context, neither explanation can be selected.

## Time and sensor context

Both products target 2021, so a simple different-reference-year explanation is not supported by the published descriptions. The Fiji test points were interpreted using 2021 annual-median Sentinel-2 and Planet NICFI RGB composites plus high-resolution Google Satellite basemaps. WorldCover v200 was generated from 2021 Sentinel-1 and Sentinel-2 time series, with cloud filtering, temporal compositing/interpolation, ancillary features and expert rules. The inputs and interpretation processes are therefore not identical even though the nominal year matches. Within-year seasonal timing, image availability, mixed pixels and changes during the year remain possible point-level issues.

WorldCover also publishes an InputQuality layer containing observation-count information for Sentinel-1 and Sentinel-2 and the proportion of invalid Sentinel-2 observations. These are input-data diagnostics, not per-pixel classification probabilities or confidence scores. They may help prioritise difficult points if the quality layer is sampled in a later review.

## Adjudication status and next evidence gate

No underlying image chips, interpreter screenshots or point-level visual decisions were available in the current comparison outputs. The WorldCover map was sampled at the single 10 m cell containing each point; the full COG tiles were range-read remotely, not downloaded and byte-hashed. The current analysis therefore supports a documentary ontology review only.

A defensible next-stage review should select a documented subset of the 89 tree–shrubland points and the 63 agriculture-to-grassland/tree points, plus the seven wetland-to-tree points. For each selected point, preserve:
1. stable sample ID and coordinates;
2. Fiji reference label and WorldCover class/code;
3. original Fiji sampling stratum;
4. source imagery, sensor/platform, acquisition date and spatial resolution;
5. a consistent image window around the point and the containing 10 m pixel;
6. visible evidence for canopy, shrub structure, herbaceous cover, crop rows, grazing, fallow, plantation and/or inundation;
7. interpreter decision, confidence, alternative label and reason;
8. whether the disagreement is primarily ontology, temporal, spatial-support, reference-interpretation or likely map-classification related.

The review should be blind to the product labels during the first interpretation pass where practical, then reveal the two map labels for comparison. Keep uncertain points as uncertain; do not force a majority-vote label. Record the imagery licence and access date, and do not redistribute high-resolution imagery unless its terms permit it.

## Current conclusion

The strongest conclusion is not that WorldCover has definitively misclassified 89 shrubland locations or 63 agriculture locations. It is that the strict eight-class comparison exposes substantial disagreement concentrated at boundaries where the two legends encode different concepts. The agriculture discrepancy has an especially clear documented ontology component because Fiji's project label includes livestock/fallow evidence while WorldCover's cropland class is annual-crop oriented and routes pasture/perennial woody crops to other classes. The tree–shrubland discrepancy is also definition-sensitive, but requires image-level evidence to determine whether it is a threshold/legend mismatch or a genuine cover classification error.

The reported overall and class-specific accuracy figures remain valid for the explicitly stated strict working crosswalk and design assumptions. They should be accompanied by this ontology qualification and must not be presented as a definitive ranking of intrinsic classifier quality.
