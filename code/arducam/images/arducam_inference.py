import cv2
import os
import json
import time

# Initialize camera with /dev/video0
cap = cv2.VideoCapture('/dev/video0')
image_dir = './arducam_images'

def draw_annotations(image, predictions):
    for pred in predictions["predictions"]:
        x, y, w, h = int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
        label = f'{pred["class"]}: {pred["confidence"]:.2f}'
        cv2.rectangle(image, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
        cv2.putText(image, label, (x - w // 2, y - h // 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

while True:
    ret, frame = cap.read()
    if ret:
        # Save the frame as an image file
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_path = os.path.join(image_dir, f'frame_{timestamp}.jpg')
        cv2.imwrite(image_path, frame)
        print(f"Saved image: {image_path}")  # Add this line to check if images are being saved

        # Run inference on the image
        inference_command = f'base64 {image_path} | curl -d @- "http://localhost:9001/target-detection-ee3x5/1?api_key=6BSPzyvwTjTvvM4RkVxd"'
        inference_result = os.popen(inference_command).read()
        predictions = json.loads(inference_result)

        # Draw annotations on the image
        annotated_image = draw_annotations(frame, predictions)
        annotated_image_path = os.path.join(image_dir, f'annotated_{timestamp}.jpg')
        cv2.imwrite(annotated_image_path, annotated_image)

        # Wait for a specific interval
        time.sleep(1)  # Capture every 1 second

cap.release()
cv2.destroyAllWindows()

