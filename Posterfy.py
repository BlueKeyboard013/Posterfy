from PIL import Image
from io import BytesIO
import os
import requests
import base64
import test
from google.cloud import vision


def create_square_collage(image_urls, art_alb_tra):
    # Load images
    sorted_urls = get_sorted_images(image_urls, art_alb_tra)

    images = []
    for k, v in sorted_urls.items():
        response = requests.get(v[3])
        img = Image.open(BytesIO(response.content))
        images.append(img)
   # Find the smallest dimension (width or height) across all images to preserve aspect ratio
    min_dimension = min(min(img.size) for img in images)
    
    # Resize images based on the smallest dimension while maintaining the aspect ratio
    resized_images = [img.resize((min_dimension, min_dimension), Image.LANCZOS) for img in images]

    # Create a new square collage
    collage_size = (min_dimension * 5, min_dimension * 10)  # 5x10 dimensions (5 width, 10 length/height)
    collage = Image.new('RGB', collage_size, (255, 255, 255))

    # Paste the images into the collage
    should_break = False
    img = 0
    for row in range(10):
        for col in range(5):
            x = col * min_dimension # x moves horizontally
            y = row * min_dimension # y moves vertically
            collage.paste(resized_images[img], (x, y))
            img += 1
            if img >= len(resized_images):
                should_break = True
                break
        if should_break:
            break

    collage.save('collage.jpg')
    return convert_to_base64(collage)


def convert_to_base64(collage):
    buffered = BytesIO()
    collage.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{img_str}"

# will have methods to sort them however the person wants to

def get_sorted_images(song_list, art_alb_tra):
    if art_alb_tra == 'artist':
        return sort_by_artist(song_list)
    elif art_alb_tra == 'album':
        return sort_by_album(song_list)
    elif art_alb_tra == 'track':
        return sort_by_track(song_list)

def sort_by_album(song_list):
    # sort alphabetically
    # should we sort by track name or album name? let's have option for both. but start with album name for now
    return dict(sorted(song_list.items(), key=lambda item: item[1]))

#
# def sort_by_genre(song_list):
#     # sort by genre, cant do this because we dont get the genre with this endpoint
#

def sort_by_track(song_list):
    return dict(sorted(song_list.items(), key=lambda item: item[1][2]))

def sort_by_artist(song_list):
    return dict(sorted(song_list.items(), key=lambda item: item[1][1]))

# def sort_by_color(song_list):
#     # group by color
#
# def randomize_order(song_list):
#     # randomize the order
