from djitellopy import Tello
import cv2
import numpy as np

# Connect to the drone
tello = Tello()
tello.connect()
print(tello.get_battery())
tello.streamon()  # Start the video stream
tello.takeoff()

# Create a window to display the video feed
cv2.namedWindow("Tello Video Feed")

# ArUco Dictionary and Detector Parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)



while True:
    frame_read = tello.get_frame_read()
    frame = frame_read.frame
    # if not ret:
    #     break

    # Convert to Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect Markers
    corners, ids, rejected = detector.detectMarkers(gray)
    # print(ids)

    # Visualize Detected Markers
    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        if ids == 0:
            break
        elif ids == 1:
            tello.flip_forward()
        elif ids == 2:
            tello.flip_back()
        elif ids == 3:
            tello.flip_left()
        elif ids == 4:
            tello.flip_right()
        else:
            continue


    # Display the frame
    cv2.imshow('ArUco Marker Detection', frame)

    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
tello.streamoff()
cv2.destroyAllWindows()
tello.land()
