// Fiji–WorldCover blind visual review: Sentinel-2 in Google Earth Engine
// Purpose: provide 2021 imagery context for the 25-point pilot.
// IMPORTANT: this script intentionally contains sample IDs and coordinates only.
// It does not contain Fiji reference labels or WorldCover predictions.

var pilotRows = [
  ['FJI2021-000071', 178.87535974897344, -16.570279101214407],
  ['FJI2021-000111', 177.3341865020335, -18.070604132759872],
  ['FJI2021-000150', 179.47840885195455, -16.739613826220094],
  ['FJI2021-000153', 178.59895429602955, -18.011359761197475],
  ['FJI2021-000206', 177.91478067932633, -17.543331234195954],
  ['FJI2021-000094', -179.9866207183685, -16.925488736232545],
  ['FJI2021-000500', -179.92306321960703, -16.75695192402456],
  ['FJI2021-000525', -179.89945686804808, -16.84132118240082],
  ['FJI2021-000526', -179.97597598726176, -16.852815330899855],
  ['FJI2021-000528', -179.96350253535988, -16.46141542838736],
  ['FJI2021-000104', 178.35272592804586, -17.79620650407022],
  ['FJI2021-000112', 177.35802990028435, -18.079358223585825],
  ['FJI2021-000124', 177.78624489856762, -17.43275592781771],
  ['FJI2021-000133', 178.7173597805704, -16.661193583074517],
  ['FJI2021-000402', 179.40474178128693, -16.533182294104442],
  ['FJI2021-000073', 179.12708040983784, -16.700178545629623],
  ['FJI2021-000264', 178.08952114924125, -19.07900831775452],
  ['FJI2021-000271', -178.94372767218618, -17.21994890614525],
  ['FJI2021-000413', 177.80529843229772, -17.54396208020703],
  ['FJI2021-000417', -179.8045034440234, -18.940936923382708],
  ['FJI2021-000088', 178.9985307151013, -16.593546954718388],
  ['FJI2021-000392', 179.7762027201951, -19.132183791406597],
  ['FJI2021-000425', 177.1329945881401, -17.309052058832933],
  ['FJI2021-000462', 178.0419074187636, -19.09715149426997],
  ['FJI2021-000505', -179.3088067411355, -17.733685844044583]
];

var points = ee.FeatureCollection(pilotRows.map(function(row) {
  return ee.Feature(
    ee.Geometry.Point([row[1], row[2]]),
    {sample_id: row[0]}
  );
}));

// Change this value to inspect another pilot location.
// Keep the blind-review sheet open separately to record observations.
var FOCUS_SAMPLE_ID = 'FJI2021-000071';

var START_DATE = '2021-01-01';
var END_DATE = '2022-01-01';
var MAX_CLOUD_PROBABILITY = 40; // Sensitivity can be checked at 30 and 50.

var sr = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED');
var cloudProbability = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY');

var filter = ee.Filter.and(
  ee.Filter.bounds(points),
  ee.Filter.date(START_DATE, END_DATE)
);

// Exclude unreliable scene-edge pixels using the 20 m and 60 m band masks.
function maskEdges(image) {
  return image.updateMask(
    image.select('B8A').mask().updateMask(image.select('B9').mask())
  );
}

var srFiltered = sr.filter(filter).map(maskEdges);
var cloudFiltered = cloudProbability.filter(filter);

// Join each surface-reflectance granule to its matching cloud-probability image.
var joined = ee.ImageCollection(ee.Join.saveFirst('cloud_mask').apply({
  primary: srFiltered,
  secondary: cloudFiltered,
  condition: ee.Filter.equals({
    leftField: 'system:index',
    rightField: 'system:index'
  })
})).filter(ee.Filter.notNull(['cloud_mask']));

function maskClouds(image) {
  var probability = ee.Image(image.get('cloud_mask')).select('probability');
  return image.updateMask(probability.lt(MAX_CLOUD_PROBABILITY));
}

var clear = joined.map(maskClouds);

var rgb = {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000, gamma: 1.15};
var focus = ee.Feature(points.filter(
  ee.Filter.eq('sample_id', FOCUS_SAMPLE_ID)
).first());
var focusGeometry = focus.geometry();

print('Blind pilot points (IDs and coordinates only)', points);
print('Sentinel-2 SR granules matched to cloud probability', clear.size());
print('Focus sample', FOCUS_SAMPLE_ID);
print('Available 2021 scene IDs at focus point',
  clear.filterBounds(focusGeometry).aggregate_array('system:index'));
print('Available 2021 acquisition dates at focus point',
  clear.filterBounds(focusGeometry).aggregate_array('system:time_start')
    .map(function(time) { return ee.Date(time).format('YYYY-MM-dd'); }));

// Annual and quarterly composites help reveal both broad cover and seasonality.
var annual = clear.filterDate('2021-01-01', '2022-01-01').median();
Map.addLayer(annual, rgb, '2021 annual median RGB', true);

var q1 = clear.filterDate('2021-01-01', '2021-04-01').median();
var q2 = clear.filterDate('2021-04-01', '2021-07-01').median();
var q3 = clear.filterDate('2021-07-01', '2021-10-01').median();
var q4 = clear.filterDate('2021-10-01', '2022-01-01').median();
Map.addLayer(q1, rgb, '2021 Q1 RGB', false);
Map.addLayer(q2, rgb, '2021 Q2 RGB', false);
Map.addLayer(q3, rgb, '2021 Q3 RGB', false);
Map.addLayer(q4, rgb, '2021 Q4 RGB', false);

// NDVI is contextual evidence only; it is not a land-cover classifier.
var ndvi = annual.normalizedDifference(['B8', 'B4']).rename('NDVI');
Map.addLayer(ndvi, {
  min: -0.2, max: 0.9,
  palette: ['8c510a', 'f6e8c3', 'c7eae5', '01665e']
}, '2021 annual median NDVI', false);

// Display pilot points without either map's class labels.
var buffers = points.map(function(feature) {
  return feature.buffer(150).copyProperties(feature, ['sample_id']);
});
Map.addLayer(buffers, {color: 'yellow'}, '150 m review context', false);
Map.addLayer(points, {color: 'red'}, 'Blind pilot points', true);
Map.addLayer(focusGeometry, {color: 'cyan'}, 'Focused point', true);
Map.centerObject(focusGeometry, 15);

// Scene metadata is printed for the currently selected focus point.
// Record scene IDs/dates and your access date in the blind-review CSV.
var focusScenes = clear.filterBounds(focusGeometry).sort('system:time_start');
print('Focus-point scene cloudiness (%)',
  focusScenes.aggregate_array('CLOUDY_PIXEL_PERCENTAGE'));
