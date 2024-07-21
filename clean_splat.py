import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
import os

# Change directory to the specified path
directory_path = r"D:\Projects_Self\AI_tools\pinokio\api\gaussian-splatting-Windows.git\output\plant\point_cloud\iteration_30000"
os.chdir(directory_path)

# Check if the directory change was successful and if the file exists
if os.getcwd() == directory_path:
    print(f"Successfully changed directory to: {directory_path}")
else:
    print(f"Failed to change directory to: {directory_path}")

file_name = "point_cloud.ply"
file_path = os.path.join(directory_path, file_name)

if os.path.isfile(file_path):
    print(f"File found: {file_path}")
else:
    print(f"File not found: {file_path}")

# Load the point cloud
pcd = o3d.io.read_point_cloud(file_name)

# Check if the point cloud has colors
if pcd.has_colors():
    print("Point cloud has colors.")
else:
    print("Point cloud does not have colors.")

# Create a visualizer
vis = o3d.visualization.Visualizer()
vis.create_window()

# Add the point cloud to the visualizer
vis.add_geometry(pcd)

# Capture the screen as an image
vis.poll_events()
vis.update_renderer()
image = vis.capture_screen_float_buffer(do_render=True)

# Convert the image to a numpy array and save it using matplotlib
image = np.asarray(image)
plt.imsave("point_cloud_image.png", image)

# Hold the window open until the user closes it
vis.run()  # This will keep the window open

# Destroy the visualizer window after the user closes it
vis.destroy_window()
