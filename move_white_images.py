import os
from PIL import Image
import shutil
from concurrent.futures import ThreadPoolExecutor

# Define the source and destination folders
source_folder = "timit_mfcc_images" # Change this to the folder containing the images to verify
destination_folder = "timit_mfcc_images_white" # Change this to the folder to move the white images to

# Ensure destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Define a tolerance for off-white colors
WHITE_THRESHOLD = 240  # Pixel values must be >= this for all R, G, B components
TOP_PIXELS_TO_CHECK = 10  # Number of top pixels to check from the top-left corner

def is_white_image(image_path):
    # Check if the top 10 pixels of the image are all white within the defined tolerance
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
    # Process all images in a single folder.
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
    # Process each folder in parallel using threads.
    folders = [os.path.join(source, folder) for folder in os.listdir(source) if os.path.isdir(os.path.join(source, folder))]
    
    with ThreadPoolExecutor() as executor:
        for folder in folders:
            executor.submit(process_folder, folder, destination)

# Execute the script
process_folders_in_parallel(source_folder, destination_folder)