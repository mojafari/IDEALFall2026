from djitellopy import Tello
import cv2

# Connect to the drone
tello = Tello()
tello.connect()
tello.streamon()  # Start the video stream

# Create a window to display the video feed
cv2.namedWindow("Tello Video Feed")

# Main loop to read and display frames
while True:
    frame_read = tello.get_frame_read()
    frame = frame_read.frame

    # Process the frame (this is where detection will go)
    # ...

    # Display the processed frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("Tello Video Feed", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
tello.streamoff()
cv2.destroyAllWindows()
