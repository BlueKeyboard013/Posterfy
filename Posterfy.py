from PIL import Image
from io import BytesIO
import os
import requests
import base64


def create_square_collage(image_urls):
    # Load images
    images = []
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        images.append(img)
   # Find the smallest dimension (width or height) across all images to preserve aspect ratio
    min_dimension = min(min(img.size) for img in images)
    
    # Resize images based on the smallest dimension while maintaining the aspect ratio
    resized_images = [img.resize((min_dimension, min_dimension), Image.LANCZOS) for img in images]

    # Create a new square collage
    collage_size = (min_dimension * 5, min_dimension * 10)  # 3x3 grid for a square collage
    collage = Image.new('RGB', collage_size, (255, 255, 255))

    # Paste the images into the collage
    img = 0
    for row in range(5):
        for col in range(10):
            x = row * min_dimension
            y = col * min_dimension
            collage.paste(resized_images[img], (x, y))
            img += 1
            if img >= len(resized_images):
                break

    return convert_to_base64(collage)


def convert_to_base64(collage):
    buffered = BytesIO()
    collage.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{img_str}"
