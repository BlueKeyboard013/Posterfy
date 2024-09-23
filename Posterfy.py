from PIL import Image

def create_square_collage(image_paths, output_path):
    # Load images
    images = [Image.open(path) for path in image_paths]

   # Find the smallest dimension (width or height) across all images to preserve aspect ratio
    min_dimension = min(min(img.size) for img in images)
    
    # Resize images based on the smallest dimension while maintaining the aspect ratio
    resized_images = [img.resize((min_dimension, min_dimension), Image.LANCZOS) for img in images]

    # Create a new square collage
    collage_size = (min_dimension * 3, min_dimension * 3)  # 3x3 grid for a square collage
    collage = Image.new('RGB', collage_size, (255, 255, 255))

    # Paste the images into the collage
    for i, img in enumerate(resized_images):
        x = (i % 3) * min_dimension
        y = (i // 3) * min_dimension
        collage.paste(img, (x, y))

    # Save the final collage
    collage.save(output_path)


# Example usage:
image_path = [
    "Pictures/IMG_8243.jpeg",
    "Pictures/IMG_8244.jpeg",
    "Pictures/IMG_8245.jpeg",
    "Pictures/IMG_8246.jpeg",
    "Pictures/IMG_8247.jpeg",
    "Pictures/IMG_8248.jpeg"
]
my_output_path = "collage.jpg"
create_square_collage(image_path, my_output_path)