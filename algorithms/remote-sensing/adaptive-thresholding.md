# Adaptive thresholding

## Purpose

A single global threshold fails when illumination or background intensity varies spatially. Adaptive thresholding computes a local threshold surface and classifies each pixel relative to its neighbourhood.

## Implemented scope

The reference implementation supports local arithmetic-mean and Gaussian-weighted thresholds, with an explicit offset and reflection padding. Foreground is defined as image > local_threshold. See [implementation](../../implementations/python/adaptive-thresholding/README.md).

## Distinctions

This is not Otsu's global between-class-variance threshold, nor is it Sauvola, Niblack or Phansalkar. Those local methods use different statistics and parameters.

## Practical cautions

Window size must match the scale of background variation and target objects. A window that is too small follows object texture; one that is too large behaves more like a global threshold. State whether the input is radiance, reflectance, an index, or a derived intensity image.
