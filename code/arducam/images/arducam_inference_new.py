import cv2
import os
import json
import time

# Initialize camera with /dev/video0
cap = cv2.VideoCapture('/dev/video0')
original_image_dir = './arducam_images'
annotated_image_dir = './arducam_images_2'

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
        original_image_path = os.path.join(original_image_dir, f'frame_{timestamp}.jpg')
        cv2.imwrite(original_image_path, frame)
        print(f"Saved image: {original_image_path}")

        # Run inference on the image
        inference_command = f'base64 {original_image_path} | curl -d @- "http://localhost:9001/helipad_detection-2zrua/4?api_key=6BSPzyvwTjTvvM4RkVxd"'
        inference_result = os.popen(inference_command).read()
        predictions = json.loads(inference_result)

        # Draw annotations on the image
        annotated_image = draw_annotations(frame, predictions)
        annotated_image_path = os.path.join(annotated_image_dir, f'annotated_{timestamp}.jpg')
        cv2.imwrite(annotated_image_path, annotated_image)
        print(f"Saved annotated image: {annotated_image_path}")

        # Wait for a specific interval
        time.sleep(1)  # Capture every 1 second

cap.release()
cv2.destroyAllWindows()

