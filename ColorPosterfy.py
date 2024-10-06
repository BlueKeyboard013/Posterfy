import os
import requests
from colorthief import ColorThief
from PIL import Image
from io import BytesIO
import shutil
from colorsys import rgb_to_hsv
import test


def get_dominant_color_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Load image from URL into memory
        image = Image.open(BytesIO(response.content))

        # Save the image temporarily into a BytesIO object for ColorThief
        image_bytes = BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes.seek(0)  # Move pointer to the start for ColorThief

        # Extract dominant color
        color_thief = ColorThief(image_bytes)
        dominant_color = color_thief.get_color(quality=1)
        return dominant_color
    else:
        return None

# sorting methods:

# sorting by hue
def rgb_to_hsv_color(color):
    r, g, b = [x / 255.0 for x in color]  # Convert to [0, 1] range
    return rgb_to_hsv(r, g, b)  # Returns (hue, saturation, value) (this is a colorsys method)

# sorting by dominant channel:
def dominant_channel(color):
    r, g, b = color
    return max(r, g, b)

def custom_sort(color):
    r, g, b = color
    if r > g and r > b:
        return (0, r)  # Red comes first, then sorted by red intensity
    elif g > r and g > b:
        return (1, g)  # Green comes second, then sorted by green intensity
    else:
        return (2, b)  # Blue comes last, then sorted by blue intensity

def get_sorted_colors(song_dict):
    for k, v in song_dict.items():
        rgb_color = v[4]
        song_dict[k][4] = custom_sort(rgb_color)

    return dict(sorted(song_dict.items(), key=lambda item: item[1][4]))
