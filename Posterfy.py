from PIL import Image
import os

def create_square_collage(image_paths, output_path):
    # Load images
    images = [Image.open(path) for path in image_paths]

   # Find the smallest dimension (width or height) across all images to preserve aspect ratio
    min_dimension = min(min(img.size) for img in images)
    
    # Resize images based on the smallest dimension while maintaining the aspect ratio
    resized_images = [img.resize((min_dimension, min_dimension), Image.LANCZOS) for img in images]

    # Create a new square collage
    collage_size = (min_dimension * 6, min_dimension * 9)  # 3x3 grid for a square collage
    collage = Image.new('RGB', collage_size, (255, 255, 255))

    # Paste the images into the collage
    img = 0
    for row in range(6):
        for col in range(9):
            x = row * min_dimension
            y = col * min_dimension
            collage.paste(resized_images[img], (x, y))
            img += 1

    # Save the final collage
    collage.save(output_path)


# Example usage:

img_paths = []
# Directory you want to traverse
directory = 'AlbumPoster'

# Traverse through files in the directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):  # Check if it's a file
        img_paths.append(file_path)


my_output_path = "collage.jpg"
create_square_collage(img_paths, my_output_path)