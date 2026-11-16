# Tasseled Cap transform

The Tasseled Cap (Kauth–Thomas) transform projects multispectral reflectance into a small set of sensor-specific linear combinations, commonly interpreted as brightness, greenness and wetness:

\[ y = (x-b)A \]

where x is the pixel's band vector, b is an optional per-band offset, and A is a supplied coefficient matrix whose columns are components. Coefficients and band order must match the sensor, product, calibration scale and processing convention. There is no universal matrix for all sensors. This implementation applies a caller-supplied matrix and does not estimate coefficients or infer band mapping.

The [NumPy implementation](../../implementations/python/pca-transform/README.md) includes shape validation and a direct matrix-product test. Tasseled Cap is distinct from PCA: the former uses externally defined sensor-specific coefficients; PCA estimates components from the sample covariance of the current dataset.

## Further reading

- Kauth, R. J. and Thomas, G. S. (1976), “The Tasseled Cap—A Graphic Description of the Spectral-Temporal Development of Agricultural Crops as Seen by Landsat,” *LARS Symposia*, paper 159.
- Crist, E. P. and Cicone, R. C. (1984), “A physically-based transformation of Thematic Mapper data—The TM Tasseled Cap,” *IEEE Transactions on Geoscience and Remote Sensing*, GE-22(3), 256–263.
