import os
import glob
from PIL import Image
import time
import math
from tqdm import tqdm
import threading
import numpy as np
import argparse

def convert_apk_to_image(apk_path, output_folder):
    # Get the filename without extension
    filename = os.path.splitext(os.path.basename(apk_path))[0]
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    # Read the apk file as binary
    with open(apk_path, 'rb') as file:
        # Convert the binary data to hexadecimal representation
        hex_data = file.read().hex()

    pixels = []
    for i in range(0, len(hex_data), 2):
        try:
            pixel = int(hex_data[i:i+2], 16)
            pixels.append(pixel)
        except ValueError:
            continue

    # Calculate the square root of the file size and take the ceiling value
    square_root = math.ceil(math.sqrt(len(pixels)))
    # Create a square_root x square_root x 3 numpy array
    image_array = np.zeros((3, square_root, square_root))
    # Put pixels inside the first (and onlythe first) channel of image (ie pixel[0] inside image[0,0,0], pixel[1] inside image[0,1,0], pixel[2] inside image[0,2,0] etc)
    # Fill in the array with pixel values
    for i in range(min(len(pixels), square_root**2)):
        row = i // square_root
        col = i % square_root
        image_array[0,row,col] = pixels[i]
        image_array[1,row,col] = pixels[i]
        image_array[2,row,col] = pixels[i]

    # Calculate the mean and standard deviation of the image array
    mean = np.mean(image_array)
    std_dev = np.std(image_array)

    # Normalize the image array
    normalized_image_array = (image_array - mean) / std_dev

    image_array = normalized_image_array.astype(np.uint8).transpose((1, 2, 0))
    
    # Resize the image array to a standard dimension (128, 128, 3)
    resized_image = Image.fromarray(image_array).resize((128, 128), Image.BILINEAR)

    # Save the resized image
    resized_image.save(f'{output_folder}/{filename}.png')


def count_outputs(output_folder):
    while True:
        # Count the number of files in the output folder (recursive)
        num_outputs = sum(len(files) for _, _, files in os.walk(output_folder))
        # Calculate the estimated time remaining based on the number of elements
        estimated_time = num_outputs * 10  # Assuming each output takes 10 seconds
        print(f"Number of outputs: {num_outputs}, Estimated time remaining: {estimated_time} seconds")
        time.sleep(10)  # Wait for 10 seconds

def process_apks(input_folder, output_folder, recursive=False):
    # If recursive is True, search recursively in the input folder for APK files
    if recursive:
        # Get the list of apk files in the input folder
        apk_files = glob.glob(f'{input_folder}/*/*.apk')
    else:
        # Get the list of apk files in the input folder
        apk_files = glob.glob(f'{input_folder}/*.apk')
    # Process each apk file
    for apk_file in tqdm(apk_files):
        convert_apk_to_image(apk_file, output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='APK to Image Converter')
    parser.add_argument('input_folder', type=str, help='Path to the input folder containing APK files')
    parser.add_argument('output_folder', type=str, help='Path to the output folder for saving the converted images')
    parser.add_argument('-r', action='store_true', help='Search recursively in input_folder for APK files')
    args = parser.parse_args()

    process_apks(args.input_folder, args.output_folder, args.r)
