import cv2
import os
import json
import time
import csv

# Initialize camera with /dev/video0
cap = cv2.VideoCapture('/dev/video0')
original_image_dir = './arducam_images'
annotated_image_dir = './arducam_images_2'
output_csv_path = './helipad_coordinates_and_directions.csv'

# Initialize CSV file
with open(output_csv_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Timestamp', 'Image', 'Helipad Center X', 'Helipad Center Y', 'Direction'])

def draw_annotations(image, predictions):
    for pred in predictions["predictions"]:
        x, y, w, h = int(pred["x"]), int(pred["y"]), int(pred["width"]), int(pred["height"])
        label = f'{pred["class"]}: {pred["confidence"]:.2f}'
        cv2.rectangle(image, (x - w // 2, y - h // 2), (x + w // 2, y + h // 2), (0, 255, 0), 2)
        cv2.putText(image, label, (x - w // 2, y - h // 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return image

def get_drone_movement_direction(image_center, helipad_center, threshold=0.25):
    image_width, image_height = image_center[0] * 2, image_center[1] * 2
    x_margin = image_width * threshold / 2
    y_margin = image_height * threshold / 2
    
    x_diff = helipad_center[0] - image_center[0]
    y_diff = helipad_center[1] - image_center[1]
    direction = ""

    if abs(x_diff) > x_margin:
        if x_diff > 0:
            direction += "Move Forward "
        else:
            direction += "Move Backwards "
    
    if abs(y_diff) > y_margin:
        if y_diff > 0:
            direction += "Move Right"
        else:
            direction += "Move Left"
    
    if direction == "":
        direction = "Centered"
    
    return direction.strip()

while True:
    ret, frame = cap.read()
    if ret:
        # Save the frame as an image file
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        original_image_name = f'frame_{timestamp}.jpg'
        original_image_path = os.path.join(original_image_dir, original_image_name)
        cv2.imwrite(original_image_path, frame)
        print(f"Saved image: {original_image_path}")

        # Run inference on the image
        inference_command = f'base64 {original_image_path} | curl -d @- "http://localhost:9001/helipad_detection-2zrua/4?api_key=6BSPzyvwTjTvvM4RkVxd"'
        inference_result = os.popen(inference_command).read()
        predictions = json.loads(inference_result)

        # Draw annotations on the image
        annotated_image = draw_annotations(frame, predictions)
        annotated_image_name = f'annotated_{timestamp}.jpg'
        annotated_image_path = os.path.join(annotated_image_dir, annotated_image_name)
        cv2.imwrite(annotated_image_path, annotated_image)
        print(f"Saved annotated image: {annotated_image_path}")

        # Calculate center of the image
        image_center = (frame.shape[1] // 2, frame.shape[0] // 2)

        # If helipad found, calculate center and direction
        if predictions["predictions"]:
            helipad = predictions["predictions"][0]
            helipad_center = (int(helipad["x"]), int(helipad["y"]))
            direction = get_drone_movement_direction(image_center, helipad_center)

            with open(output_csv_path, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([timestamp, original_image_name, helipad_center[0], helipad_center[1], direction])

        # Wait for a specific interval
        time.sleep(1)  # Capture every 1 second

cap.release()
cv2.destroyAllWindows()
