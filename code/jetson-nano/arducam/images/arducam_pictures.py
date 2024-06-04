import cv2
import time
import os

# Initialize camera with /dev/video0
cap = cv2.VideoCapture('/dev/video0')
image_dir = './arducam_images'

while True:
    ret, frame = cap.read()
    if ret:
        # Save the frame as an image file
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_path = os.path.join(image_dir, f'frame_{timestamp}.jpg')
        cv2.imwrite(image_path, frame)
        
        # Optional: Run inference on the image
        # os.system(f'base64 {image_path} | curl -d @- "http://localhost:9001/target-detection-ee3x5/1?api_key=6BSPzyvwTjTvvM4RkVxd"')
        
        # Wait for a specific interval
        time.sleep(1)  # Capture every 2 seconds

cap.release()
cv2.destroyAllWindows()

