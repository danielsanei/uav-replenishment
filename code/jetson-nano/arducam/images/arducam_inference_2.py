import cv2
import os
import json

# Directories for images
image_dir = './arducam_images'
annotated_image_dir = './arducam_images_2'

# Ensure the output directory exists
if not os.path.exists(annotated_image_dir):
    os.makedirs(annotated_image_dir)

def draw_annotations(image, predictions):
    for pred in predictions["predictions"]:
        x, y, w, h = int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
        label = f'{pred["class"]}: {pred["confidence"]:.2f}'
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return image

# Process all images in the directory
for image_name in os.listdir(image_dir):
    if image_name.endswith('.jpg'):
        image_path = os.path.join(image_dir, image_name)
        
        # Read the image
        frame = cv2.imread(image_path)

        # Run inference on the image
        inference_command = f'base64 {image_path} | curl -d @- "http://localhost:5000/v1/object-detection/yolov5"'
        inference_result = os.popen(inference_command).read()
        
        # Ensure the result is not empty
        if not inference_result:
            print(f"Failed to get inference result for {image_name}")
            continue
        
        predictions = json.loads(inference_result)

        # Draw annotations on the image
        annotated_image = draw_annotations(frame, predictions)
        annotated_image_path = os.path.join(annotated_image_dir, f'annotated_{image_name}')
        
        # Save the annotated image
        cv2.imwrite(annotated_image_path, annotated_image)
        
        # Optional: Remove the original unannotated image
        # os.remove(image_path)

print("Processing complete.")

