from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np

def colorize_matrix(matrix):
    # Define colors
    dark_blue = (0, 0, 139)  # Dark blue in RGB format
    yellow = (255, 255, 0)   # Yellow in RGB format
    
    # Create an empty image matrix
    height, width = matrix.shape
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Convert matrix values to colors
    for i in range(height):
        for j in range(width):
            if matrix[i, j] == 0:
                image[i, j] = dark_blue
            else:
                image[i, j] = yellow
    
    return image

# Define output video file name
output_file = 'output/plant_plus_mask.mp4'

# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 30.0  # Frames per second
out = cv2.VideoWriter(output_file, fourcc, fps, (2160, 1920))

# to add text on video
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (255, 255, 255)  # White color in BGR format
thickness = 2
line_type = cv2.LINE_AA

# Load the YOLOv8 segmentation model
model = YOLO("yolov8l-seg.pt")  # Make sure to use a model trained for segmentation
class_names = model.module.names if hasattr(model, 'module') else model.names

# Open the video file
video_path = 'data/plant.mp4'
cap = cv2.VideoCapture(video_path)

mask_list = []
images_list = []
save_mask_list = []

selected_object_idx = 0
frame_idx = -1
while cap.isOpened():
    frame_idx +=1
    campter_frame = ((frame_idx)%int(fps) == 0)
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference on the frame
    results = model.track(frame, persist=True)

    # plot results
    frame_ = results[0].plot()
    wanted_mask = results[0].masks[selected_object_idx].data.cpu().numpy()[0]
    mask_list.append(wanted_mask)
    wanted_mask_color = colorize_matrix(wanted_mask)
    object_name_idx = int(results[0].boxes.cls[selected_object_idx].numpy())
    object_name = class_names[object_name_idx]    
    
    # Visualize
    mask_reshape = cv2.resize(wanted_mask_color, [frame_.shape[1], frame_.shape[0]])
    combined_image = cv2.hconcat([frame_, mask_reshape])
    cv2.putText(combined_image, object_name, [frame_.shape[0], 50], font, font_scale, font_color, thickness, line_type)

    cv2.imshow('frame', cv2.resize(combined_image, [640, 480]))
    out.write(np.clip(combined_image, 0, 255).astype(np.uint8))
    
    if campter_frame:
        images_list.append(frame)
        save_mask_list.append(wanted_mask)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

mask_list.append(wanted_mask)
save_mask_list.append(wanted_mask)
np.save('mask_output_total.npy', np.array(mask_list))
np.save('output/mask_output.npy', np.array(save_mask_list))
for idx in range(len(images_list)):
    if idx +1 >= 10:
        cv2.imwrite(f'output/0{idx+1}.png', images_list[idx])
    else:
        cv2.imwrite(f'output/00{idx+1}.png', images_list[idx])

cap.release()
out.release()
cv2.destroyAllWindows()