"""SLIC-style superpixel clustering for raster feature vectors."""
import math

def _image(features):
    if isinstance(features, (str, bytes)) or not isinstance(features, (list, tuple)) or not features:
        raise ValueError("features must be a non-empty HxWxC sequence")
    if any(not isinstance(row, (list, tuple)) or not row for row in features):
        raise ValueError("each image row must be a non-empty sequence")
    width = len(features[0])
    if any(len(row) != width for row in features):
        raise ValueError("image must be rectangular")
    channels = None
    image = []
    for row in features:
        out_row = []
        for pixel in row:
            if isinstance(pixel, (str, bytes)) or not isinstance(pixel, (list, tuple)) or not pixel:
                raise ValueError("each pixel must be a non-empty feature vector")
            if channels is None:
                channels = len(pixel)
            if len(pixel) != channels:
                raise ValueError("all pixels must have the same feature dimension")
            values = []
            for value in pixel:
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                    raise ValueError("pixel features must be finite numeric values")
                values.append(float(value))
            out_row.append(values)
        image.append(out_row)
    return image, len(image), width, channels

def _gradient(image, row, col):
    h, w = len(image), len(image[0])
    centre = image[row][col]
    total = 0.0
    if col + 1 < w:
        total += math.fsum((a-b)**2 for a,b in zip(centre, image[row][col+1]))
    if row + 1 < h:
        total += math.fsum((a-b)**2 for a,b in zip(centre, image[row+1][col]))
    return total

def slic_superpixels(features, *, region_size=10, compactness=10.0, max_iterations=10, tolerance=1e-3):
    """Cluster feature pixels in joint feature/coordinate space."""
    image, height, width, channels = _image(features)
    if isinstance(region_size, bool) or not isinstance(region_size, int) or region_size < 1:
        raise ValueError("region_size must be a positive integer")
    if isinstance(compactness, bool) or not isinstance(compactness, (int, float)) or not math.isfinite(compactness) or compactness <= 0:
        raise ValueError("compactness must be finite and positive")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and non-negative")
    rows = list(range(region_size//2, height, region_size)) or [height//2]
    cols = list(range(region_size//2, width, region_size)) or [width//2]
    centres = []
    for row in rows:
        for col in cols:
            candidates = [(rr, cc) for rr in range(max(0,row-1),min(height,row+2))
                          for cc in range(max(0,col-1),min(width,col+2))]
            seed_row, seed_col = min(candidates, key=lambda rc: (_gradient(image,*rc),rc[0],rc[1]))
            centres.append([float(seed_row), float(seed_col), *image[seed_row][seed_col]])
    spatial_weight = (float(compactness) / region_size) ** 2
    labels = [[-1 for _ in range(width)] for _ in range(height)]
    iterations = 0
    for iteration in range(max_iterations):
        distances = [[math.inf for _ in range(width)] for _ in range(height)]
        labels = [[-1 for _ in range(width)] for _ in range(height)]
        for label, centre in enumerate(centres):
            cr, cc = centre[0], centre[1]
            r0, r1 = max(0,int(math.floor(cr-2*region_size))), min(height,int(math.ceil(cr+2*region_size+1)))
            c0, c1 = max(0,int(math.floor(cc-2*region_size))), min(width,int(math.ceil(cc+2*region_size+1)))
            for row in range(r0,r1):
                for col in range(c0,c1):
                    colour = math.fsum((a-b)**2 for a,b in zip(image[row][col],centre[2:]))
                    spatial = (row-cr)**2 + (col-cc)**2
                    distance = colour + spatial_weight*spatial
                    if distance < distances[row][col]:
                        distances[row][col] = distance
                        labels[row][col] = label
        for row in range(height):
            for col in range(width):
                if labels[row][col] < 0:
                    label = min(range(len(centres)), key=lambda k: (
                        math.fsum((a-b)**2 for a,b in zip(image[row][col],centres[k][2:])) +
                        spatial_weight*((row-centres[k][0])**2+(col-centres[k][1])**2), k))
                    labels[row][col] = label
        sums = [[0.0 for _ in range(2+channels)] for _ in centres]
        counts = [0 for _ in centres]
        for row in range(height):
            for col in range(width):
                label = labels[row][col]
                sums[label][0] += row
                sums[label][1] += col
                for channel, value in enumerate(image[row][col]):
                    sums[label][2+channel] += value
                counts[label] += 1
        updated = []
        max_shift = 0.0
        for index, centre in enumerate(centres):
            if counts[index] == 0:
                updated.append(centre)
                continue
            new = [value/counts[index] for value in sums[index]]
            shift = math.sqrt(math.fsum((a-b)**2 for a,b in zip(centre,new)))
            max_shift = max(max_shift, shift)
            updated.append(new)
        centres = updated
        iterations = iteration + 1
        if max_shift <= tolerance:
            break
    return {"labels": labels, "centres": centres, "iterations": iterations}
