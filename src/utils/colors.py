"""
Color-related utilities.
"""

import io
import random

import numpy
import scipy.cluster
import sklearn.cluster
from PIL import Image

__all__ = (
    "rgb",
    "int_to_hex",
    "hex",
    "get_dominant_color",
    "get_random_dominant_color",
    "get_dominant_colors"
)

def rgb(r: int = None, g: int = None, b: int = None) -> int:
    """Convert RGB to hex code."""
    return r << 16 | g << 8 | b

def int_to_hex(int: int, upper: bool = True) -> str:
    """Convert an integer to string hex code."""
    return f"#{int:06X}" if upper else f"#{int:06x}"

def hex(hex: int) -> tuple[int, int, int]:
    """Convert a hex code to a `(r, g, b)` tuple."""
    r = hex >> 16
    g = hex >> 8 & 0xFF
    b = hex & 0xFF
    return (r, g, b)

def get_dominant_color(bytes: bytes):
    """Get the most dominant color in a bytes-like image file"""
    return get_dominant_colors(bytes)[0]

def get_random_dominant_color(bytes: bytes):
    """Get a random dominant color in a bytes-like image file"""
    colors = get_dominant_colors(bytes)[:5]
    return random.choice(colors)

def get_dominant_colors(bytes: bytes):
    """Get the dominant colors in a bytes-like image file (sorted from high to low)"""
    image = Image.open(io.BytesIO(bytes))
    image = image.resize((150, 150)) # optional, to reduce time
    ar = numpy.asarray(image)
    shape = ar.shape
    ar = ar.reshape(numpy.product(shape[:2]), shape[2]).astype(float)

    kmeans = sklearn.cluster.MiniBatchKMeans(
        n_clusters=10,
        init="k-means++",
        max_iter=20,
        random_state=1000
    ).fit(ar)
    codes = kmeans.cluster_centers_

    vecs, _dist = scipy.cluster.vq.vq(ar, codes)      # assign codes
    counts, _bins = numpy.histogram(vecs, len(codes)) # count occurrences

    colors = []
    for index in numpy.argsort(counts)[::-1]:
        color = [int(code) for code in codes[index]]
        del color[3]
        color = tuple(color)
        
        colors.append(rgb(*color))
    
    return colors # colors in order of dominance