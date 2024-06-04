import cv2

# Initialize camera with /dev/video0
cap = cv2.VideoCapture('/dev/video0')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('drone_feed.avi', fourcc, 20.0, (640, 480))

max_frames = 7200  # Record 3600 frames (~3 minutes at 20 fps)
frame_count = 0

while cap.isOpened() and frame_count < max_frames:
    ret, frame = cap.read()
    if ret:
        out.write(frame)
        frame_count += 1
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

