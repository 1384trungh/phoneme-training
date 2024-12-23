import os
from PIL import Image
import shutil
from concurrent.futures import ThreadPoolExecutor

# Define the source and destination folders
source_folder = "timit_mfcc_images_test"
destination_folder = "timit_mfcc_images_test_white"

# Ensure destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Define a tolerance for off-white colors
WHITE_THRESHOLD = 240  # Pixel values must be >= this for all R, G, B components
TOP_PIXELS_TO_CHECK = 10  # Number of top pixels to check from the top-left corner

def is_white_image(image_path):
    """Check if the top 10 pixels of the image are all white within the defined tolerance."""
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            width, _ = img.size

            # Ensure the image has enough width for the top 10 pixels
            pixels_to_check = min(TOP_PIXELS_TO_CHECK, width)

            # Get the top 10 pixels from the top-left corner
            top_pixels = [img.getpixel((x, 0)) for x in range(pixels_to_check)]

            # Check if all the top pixels are close to white
            return all(all(channel >= WHITE_THRESHOLD for channel in pixel) for pixel in top_pixels)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def process_folder(folder, destination):
    """Process all images in a single folder."""
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                if is_white_image(file_path):
                    try:
                        # Move the file to the destination folder
                        dest_path = os.path.join(destination, os.path.relpath(file_path, source_folder))
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.move(file_path, dest_path)
                        print(f"Moved: {file_path} -> {dest_path}")
                    except Exception as e:
                        print(f"Error moving file {file_path}: {e}")

def process_folders_in_parallel(source, destination):
    """Process each folder in parallel using threads."""
    folders = [os.path.join(source, folder) for folder in os.listdir(source) if os.path.isdir(os.path.join(source, folder))]
    
    with ThreadPoolExecutor() as executor:
        for folder in folders:
            executor.submit(process_folder, folder, destination)

# Execute the script
process_folders_in_parallel(source_folder, destination_folder)

# import os
# from PIL import Image
# import shutil

# # Define the source folder
# source_folder = "timit_mfcc_images"
# destination_folder = "timit_mfcc_images_white"

# # Ensure destination folder exists
# os.makedirs(destination_folder, exist_ok=True)

# # Define a tolerance for off-white colors
# WHITE_THRESHOLD = 240  # Pixel values must be >= this for all R, G, B components
# WHITE_PERCENTAGE = 0.90  # At least 90% of pixels must be close to white

# def is_white_image(image_path):
#     """Check if the image is mostly white within the defined tolerance."""
#     with Image.open(image_path) as img:
#         img = img.convert("RGB")
#         pixels = list(img.getdata())
#         total_pixels = len(pixels)
        
#         # Count pixels close to white
#         white_pixels = sum(
#             1 for pixel in pixels if all(channel >= WHITE_THRESHOLD for channel in pixel)
#         )
        
#         # Calculate percentage of white pixels
#         white_ratio = white_pixels / total_pixels
        
#         # If the image is white, print debug info
#         if white_ratio >= WHITE_PERCENTAGE:
#             print(f"Identified as white: {image_path}")
#             # print(f"Total pixels: {total_pixels}, White pixels: {white_pixels}, White ratio: {white_ratio:.2f}")
        
#         return white_ratio >= WHITE_PERCENTAGE

# def process_images(source, destination):
#     for root, _, files in os.walk(source):
#         for file in files:
#             if file.lower().endswith(('.png', '.jpg', '.jpeg')):
#                 file_path = os.path.join(root, file)
#                 try:
#                     if is_white_image(file_path):
#                         # Move the file to the destination folder
#                         shutil.move(file_path, os.path.join(destination, file))
#                 except Exception as e:
#                     print(f"Error processing file {file_path}: {e}")

# # Execute the script
# process_images(source_folder, destination_folder)
