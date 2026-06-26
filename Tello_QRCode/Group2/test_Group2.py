import cv2
from djitellopy import Tello
import numpy as np
import threading
import time

# --- Shared Resources for Threading ---
frame_lock = threading.Lock()
latest_frame = None
is_running = True
# A shared variable to store the latest command decoded from a QR code
latest_command = None
command_lock = threading.Lock()

# Connect to the drone in the main thread initially
tello = Tello()
tello.connect()
print(f"Battery level: {tello.get_battery()}")


# Thread for fetching video frames from the Tello
def video_read_thread():
    global latest_frame
    global is_running

    tello.streamon()  # Start the video stream on this thread
    while is_running:
        frame_read = tello.get_frame_read()
        if frame_read.frame is not None:
            with frame_lock:
                latest_frame = frame_read.frame
        time.sleep(0.01)  # Small sleep to prevent burning CPU
    tello.streamoff()


# Thread for handling drone commands based on decoded QR codes
def command_thread_function():
    global is_running
    global latest_command

    try:
        tello.takeoff()
        # tello.rotate_clockwise(30)


        while is_running:
            command = None
            with command_lock:
                command = latest_command
                # Reset the command after reading it to process one command at a time
                latest_command = None

            if command:
                if command == "Door 1":
                    print("QR code 'stop' detected. Landing drone.")
                    is_running = False  # Signal main loop and video thread to stop
                elif command == "Door 2":
                    print("QR code 'Door 2' detected, unknown location/door, CW 60.")
                    tello.rotate_clockwise(60)
                elif command == "Door 3":
                    print("QR code 'Door 3' detected, unknown location/door, CW 60.")
                    tello.rotate_clockwise(60)
                # elif command == "flip_left":
                #     print("QR code 'flip_left' detected.")
                #     tello.flip_left()
                # elif command == "flip_right":
                #     print("QR code 'flip_right' detected.")
                #     tello.flip_right()
                # # Add more custom commands here
                else:
                    print(f"Detected unknown location/door: {command}")
                    # break

            # Small sleep to prevent burning CPU
            time.sleep(0.1)

    except Exception as e:
        print(f"An error occurred in the command thread: {e}")
    finally:
        # Ensure the drone lands even if an error occurred
        if tello.is_flying:
            tello.land()
        is_running = False  # Ensure all loops stop


# --- Main Program Execution ---
if __name__ == "__main__":
    # Create and start the threads
    video_thread = threading.Thread(target=video_read_thread, daemon=True)
    command_thread = threading.Thread(target=command_thread_function)

    video_thread.start()
    command_thread.start()

    # Create a QR code detector in the main thread
    qr_detector = cv2.QRCodeDetector()
    cv2.namedWindow("Tello Video Feed")

    try:
        while is_running:
            # Get the latest frame from the video thread
            frame_to_process = None
            with frame_lock:
                frame_to_process = latest_frame

            if frame_to_process is not None:
                # Detect and decode QR codes in the frame
                decoded_info, points, _ = qr_detector.detectAndDecode(frame_to_process)

                # Visualize and update shared command variable
                if points is not None:
                    # Draw a bounding box around the QR code
                    frame_to_process = cv2.polylines(frame_to_process, np.int32([points]), True, (0, 255, 0), 3)

                    if decoded_info:
                        # Display the decoded information
                        cv2.putText(frame_to_process, decoded_info, (int(points[0][0][0]), int(points[0][0][1]) - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        # Store the command in the shared variable for the command thread to pick up
                        with command_lock:
                            latest_command = decoded_info
                    else:
                        print("QR code detected but could not be decoded.")

                # Display the frame
                cv2.imshow("Tello Video Feed", frame_to_process)

            # Check for keyboard 'q' press to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                is_running = False

    finally:
        # Ensure all threads are joined and resources released
        command_thread.join()
        video_thread.join(timeout=1)
        cv2.destroyAllWindows()
        tello.end()  # Use tello.end() for safe shutdown
        print("Program ended safely.")
