import cv2
from djitellopy import Tello
import numpy as np

# Connect to the drone
tello = Tello()
tello.connect()
print(f"Battery level: {tello.get_battery()}")
tello.streamon()  # Start the video stream
tello.takeoff()

# Create a window to display the video feed
cv2.namedWindow("Tello Video Feed")

# Create a QR code detector
qr_detector = cv2.QRCodeDetector()

while True:
    frame_read = tello.get_frame_read()
    frame = frame_read.frame

    if frame is None or frame.size == 0:
        continue

    # Detect and decode QR codes in the frame
    decoded_info, points, _ = qr_detector.detectAndDecode(frame)

    # Visualize and act on detected QR codes
    if points is not None:
        # Draw a bounding box around the QR code
        frame = cv2.polylines(frame, np.int32([points]), True, (0, 255, 0), 3)

        if decoded_info:
            # Display the decoded information
            cv2.putText(frame, decoded_info, (int(points[0][0][0]), int(points[0][0][1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Perform actions based on the decoded QR code data
            if decoded_info == "stop":
                print("QR code 'stop' detected. Landing drone.")
                tello.land()
                break  # Exit the loop to end the program
            elif decoded_info == "flip_forward":
                print("QR code 'flip_forward' detected.")
                tello.flip_forward()
            elif decoded_info == "flip_back":
                print("QR code 'flip_back' detected.")
                tello.flip_back()
            elif decoded_info == "flip_left":
                print("QR code 'flip_left' detected.")
                tello.flip_left()
            elif decoded_info == "flip_right":
                print("QR code 'flip_right' detected.")
                tello.flip_right()
            # Add more custom commands here
            else:
                print(f"Detected unknown QR code: {decoded_info}")
        else:
            print("QR code detected but could not be decoded.")

    # Display the frame
    cv2.imshow("Tello Video Feed", frame)

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
tello.streamoff()
cv2.destroyAllWindows()
tello.land()
