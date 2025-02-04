import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# Define the source folder
source_folder = "timit_mfcc_images" # Change this to the folder containing the images to verify

# Define a tolerance for off-white colors
WHITE_THRESHOLD = 240  # Pixel values must be >= this for all R, G, B components
PIXEL_COUNT_TO_CHECK = 10  # Number of pixels to check from the top left

def verify_image(image_path):
    # Check if the top 10 pixels of the image are all white within the defined tolerance
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            width, height = img.size

            # Ensure we only check as many pixels as the image width allows
            pixels_to_check = min(PIXEL_COUNT_TO_CHECK, width)
            top_pixels = [img.getpixel((x, 0)) for x in range(pixels_to_check)]

            # Check if all channels of each top pixel meet the white threshold
            all_white = all(all(channel >= WHITE_THRESHOLD for channel in pixel) for pixel in top_pixels)
            
            if all_white:
                print(f"Image is white: {image_path}")
    except Exception as e:
        print(f"Error verifying file {image_path}: {e}")

def verify_images(source):
    # Verify all images in the source folder for white top pixels using multithreading
    image_files = []
    
    # Walk through the directory structure and gather image file paths
    for root, _, files in os.walk(source):
        print(f"Entering folder: {root}")
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                image_files.append(file_path)

    # Use a ThreadPoolExecutor to verify images concurrently
    with ThreadPoolExecutor() as executor:
        executor.map(verify_image, image_files)

# Execute the script
if __name__ == "__main__":
    verify_images(source_folder)
