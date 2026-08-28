"""
IDEAL Fall 2026 - Tello Video Stream

Learning objectives:
- Start the Tello camera
- Receive video frames
- Display frames using OpenCV
- Understand the basic computer-vision workflow

Press Q to close the video window.
"""

from djitellopy import Tello
import cv2

# Connect to the Tello
tello = Tello()
tello.connect()

print("Battery:", tello.get_battery(), "%")

# Start video stream
tello.streamon()

# Get access to the video frames
frame_read = tello.get_frame_read()

# Create a video window
cv2.namedWindow("Tello Video Feed", cv2.WINDOW_NORMAL)

while True:

    # Get the current frame
    frame = frame_read.frame

    # Display the frame
    cv2.imshow("Tello Video Feed", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Stop video stream
tello.streamoff()

# Close OpenCV windows
cv2.destroyAllWindows()

print("Video stream stopped.")
