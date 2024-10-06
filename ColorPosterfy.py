import os
import requests
from colorthief import ColorThief
from PIL import Image
from io import BytesIO
import shutil


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

def classify_color(rgb):
    r, g, b = rgb
    if r > g and r > b:
        return "Red"
    elif g > r and g > b:
        return "Green"
    elif b > r and b > g:
        return "Blue"
    else:
        return "Other"

