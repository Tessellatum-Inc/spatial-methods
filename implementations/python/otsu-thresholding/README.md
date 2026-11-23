# Otsu global thresholding

NumPy implementation of exact observed-level, two-class global Otsu thresholding.

Run with:

    python -m pip install -r requirements.txt
    pytest -q

API:

    from otsu_threshold import otsu_threshold, otsu_binarize
    threshold = otsu_threshold(image, mask=valid_pixels)
    threshold, foreground = otsu_binarize(image, mask=valid_pixels)

The algorithm sorts unique finite observed values and evaluates every split,
avoiding histogram-bin quantisation. It costs O(n log n) time and O(n) memory;
a histogram implementation may be preferable for very large bounded-integer
images. Foreground means strictly greater than the threshold. Invalid,
non-finite and masked pixels remain False. A constant image returns its sole
value and produces an empty foreground mask.

This is not adaptive/local or multi-level thresholding. Illumination gradients,
shadows, overlapping class distributions and spatial context can make a
single global threshold unsuitable. Calibrate imagery and apply quality masks
before interpretation.
