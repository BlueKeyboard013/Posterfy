import os
from uuid import bytes_

import requests
from colorthief import ColorThief
from PIL import Image
from io import BytesIO
import shutil
from colorsys import rgb_to_hsv
import test
import cv2
import numpy as np
from sklearn.cluster import KMeans
import os


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

# analyze specific regions
def analyze_regions(image_url):
    # Open the image
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Define the region of interest (ROI) as a box: (left, upper, right, lower)
    box = (0, 0, 320, 320)  # Example coordinates (crop 200x200 region)
    box1 = (320, 0, 640, 320)
    box2 = (0, 320, 320, 640)
    box3 = (320, 320, 640, 640)

    boxes = [box, box1, box2, box3]

    colors = []
    for my_box in boxes:
        region = img.crop(my_box)

        # Show the cropped region (optional)
        region.show()

        # Convert cropped region to RGB and calculate the average color
        region = region.convert('RGB')
        pixels = list(region.getdata())
        avg_color = tuple(sum(channel) // len(pixels) for channel in zip(*pixels))
        colors.append(avg_color)
        print(f"Average color in the selected region: {avg_color}")

# sort by most populous color (using k-means clustering)
def process_image(img_url, num_clusters=5):
    response = requests.get(img_url)
    bytes_img = Image.open(BytesIO(response.content))
    opencv_img = convert_to_opencv(bytes_img)
    return get_dominant_color(opencv_img)

def get_dominant_color(image, num_clusters=5):
    # Reshape the image to be a list of pixels
    pixels = image.reshape((-1, 3))

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(pixels)

    # Get the cluster centers (dominant colors) and labels
    dominant_colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_

    # Count the number of pixels in each cluster to find the most populous color
    counts = np.bincount(labels)

    # Find the index of the most populous cluster
    most_populous_color_index = np.argmax(counts)

    # Return the most populous color
    return [dominant_colors[most_populous_color_index][0], dominant_colors[most_populous_color_index][1], dominant_colors[most_populous_color_index][2]]

def convert_to_opencv(img):
    open_cv_image = np.array(img)
    return open_cv_image

def get_sorted_colors(song_dict):
    for k, v in song_dict.items():
        rgb_color = process_image(v[3])
        song_dict[k][4] = rgb_to_hsv_color(rgb_color)

    return dict(sorted(song_dict.items(), key=lambda item: item[1][4]))

# pic1 = test.song_dict4[11][3]
#
# print(process_image(pic1))