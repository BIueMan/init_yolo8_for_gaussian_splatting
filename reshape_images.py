import cv2
import os

# Define input and output directories
input_dir = 'output/small'
output_dir = 'output/reshape'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Desired dimensions
new_width = 1039
new_height = 1848

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    # Construct full file path
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)
    
    # Read the image
    image = cv2.imread(input_path)
    
    # Check if the image was successfully read
    if image is None:
        print(f"Failed to load {input_path}")
        continue
    
    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))
    
    # Save the resized image to the output directory
    cv2.imwrite(output_path, resized_image)
    print(f"Resized and saved {filename}")

print("Resizing complete.")
