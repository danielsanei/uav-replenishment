import cv2
import os
import json
import base64
import requests

# Directories for images
image_dir = './test_infer'
annotated_image_dir = './arducam_images_2'

# Ensure the output directory exists
if not os.path.exists(annotated_image_dir):
    os.makedirs(annotated_image_dir)

def draw_annotations(image, predictions):
    for pred in predictions["predictions"]:
        x, y, w, h = int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
        label = f'{pred["class"]}: {pred["confidence"]:.2f}'
        cv2.rectangle(image, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
        cv2.putText(image, label, (x - w // 2, y - h // 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

# Process all images in the directory
for image_name in os.listdir(image_dir):
    if image_name.endswith('.jpg') or image_name.endswith('.jpeg'):
        image_path = os.path.join(image_dir, image_name)

        # Read the image
        frame = cv2.imread(image_path)

        # Run inference on the image
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        response = requests.post(
            "https://detect.roboflow.com/helipad_detection-2zrua/1?api_key=[YOUR_API_KEY]",
            data=encoded_image,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code != 200:
            print(f"Failed to get inference result for {image_name}")
            continue
        
        predictions = response.json()

        # Draw annotations on the image
        annotated_image = draw_annotations(frame, predictions)
        annotated_image_path = os.path.join(annotated_image_dir, f'annotated_{image_name}')
        cv2.imwrite(annotated_image_path, annotated_image)

print("Processing complete.")

