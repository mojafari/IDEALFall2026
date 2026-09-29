import threading
import time
import cv2
from djitellopy import Tello
import numpy as np

# --- Shared Variables and Locks ---
# Use a shared variable to store the latest frame and a lock for thread-safe access.
frame_lock = threading.Lock()
latest_frame = None
is_running = True  # Flag to signal all threads to stop


# Thread for fetching video frames from the Tello
def video_read_thread(tello_instance):
    global latest_frame
    global is_running

    tello_instance.streamon()
    while is_running:
        frame_read = tello_instance.get_frame_read()
        if frame_read.frame is not None:
            with frame_lock:
                latest_frame = frame_read.frame
        # Sleep briefly to prevent this thread from consuming 100% CPU
        time.sleep(0.01)
    tello_instance.streamoff()


# Thread for handling QR code detection and drone commands
def qr_detection_thread(tello_instance):
    global latest_frame
    global is_running

    qr_detector = cv2.QRCodeDetector()

    # Give the video thread a moment to start and get the first frame
    time.sleep(1)

    while is_running:
        frame_to_process = None
        with frame_lock:
            if latest_frame is not None:
                frame_to_process = latest_frame.copy()

        if frame_to_process is not None:
            # Detect and decode QR codes in the frame
            decoded_info, points, _ = qr_detector.detectAndDecode(frame_to_process)

            if points is not None and decoded_info:
                print(f"Detected QR code: {decoded_info}")
                # Perform actions based on the decoded QR code data
                try:
                    if decoded_info == "stop":
                        print("QR code 'stop' detected. Landing drone.")
                        tello_instance.land()
                        is_running = False  # Signal main loop to end
                    elif decoded_info == "up":
                        print("QR code 'flip_forward' detected.")
                        tello_instance.flip_forward()
                    elif decoded_info == "down":
                        print("QR code 'flip_back' detected.")
                        tello_instance.flip_back()
                    elif decoded_info == "flip_left":
                        print("QR code 'flip_left' detected.")
                        tello_instance.flip_left()
                    elif decoded_info == "flip_right":
                        print("QR code 'flip_right' detected.")
                        tello_instance.flip_right()
                    # Add more custom commands here
                except Exception as e:
                    print(f"Error executing drone command: {e}")

        # Sleep briefly to prevent high CPU usage
        time.sleep(0.05)


# --- Main Program Execution ---
if __name__ == "__main__":
    # Initialize Tello object
    tello = Tello()
    tello.connect()
    print("Battery:", tello.get_battery(), "%")

    # Create and start the threads
    # Pass the tello instance to the thread functions
    video_thread = threading.Thread(target=video_read_thread, args=(tello,), daemon=True)
    qr_thread = threading.Thread(target=qr_detection_thread, args=(tello,))

    video_thread.start()

    # Auto takeoff before starting the detection logic
    tello.takeoff()

    qr_thread.start()

    try:
        # The main thread handles displaying the video feed
        while is_running:
            frame_to_display = None
            with frame_lock:
                frame_to_display = latest_frame

            if frame_to_display is not None:
                # Resize for better viewing experience
                display_frame = cv2.resize(frame_to_display, (960, 720))
                cv2.imshow("Tello Video Feed", display_frame)

            # Check for keyboard 'q' press to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                is_running = False

    finally:
        # --- Clean up ---
        print("Cleaning up and landing drone...")
        is_running = False  # Ensure all threads know to stop
        qr_thread.join()  # Wait for QR thread to finish (should land the drone)
        video_thread.join(timeout=2)  # Wait briefly for video thread
        cv2.destroyAllWindows()
        tello.end()  # Disconnect from the Tello
        print("Program ended safely.")

