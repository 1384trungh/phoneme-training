import os
from PIL import Image

# Define the source folder
source_folder = "timit_mfcc_images_white"

# Define a tolerance for off-white colors
WHITE_THRESHOLD = 240  # Pixel values must be >= this for all R, G, B components
PIXEL_COUNT_TO_CHECK = 10  # Number of pixels to check from the top left

def verify_image(image_path):
    """Check if the top 10 pixels of the image are all white within the defined tolerance."""
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        width, height = img.size
        
        # Ensure the image has at least 10 pixels in width
        pixels_to_check = min(PIXEL_COUNT_TO_CHECK, width)
        
        # Get the top 10 pixels from the top-left corner
        top_pixels = [img.getpixel((x, 0)) for x in range(pixels_to_check)]
        
        # Check if all the top pixels are close to white
        all_white = all(all(channel >= WHITE_THRESHOLD for channel in pixel) for pixel in top_pixels)
        
        if all_white is False:
            print(f"Image is colored: {image_path}")

def verify_images(source):
    """Verify all images in the source folder for white top pixels."""
    for root, _, files in os.walk(source):
        print(f"Entering folder: {root}")  # Print when entering a new folder
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                try:
                    verify_image(file_path)
                except Exception as e:
                    print(f"Error verifying file {file_path}: {e}")

# Execute the script
verify_images(source_folder)
