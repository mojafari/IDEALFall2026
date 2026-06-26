import threading
import time
import cv2
from djitellopy import Tello
from ultralytics import YOLO

# Use a shared variable to store the latest frame
# and a lock to ensure thread-safe access.
frame_lock = threading.Lock()
latest_frame = None
is_running = True

# --- YOLO Setup ---
# Load a pre-trained YOLOv8 model. 'yolov8n.pt' is the nano version, which is
# fast and suitable for real-time applications like this.
# You can choose a larger model for more accuracy if needed, but it will be slower.
model = YOLO('yolov8n.pt')

# Thread for fetching video frames from the Tello
def video_read_thread():
    global latest_frame
    global is_running

    tello.streamon()
    while is_running:
        frame_read = tello.get_frame_read()
        if frame_read.frame is not None:
            with frame_lock:
                latest_frame = frame_read.frame
        time.sleep(0.01)
    tello.streamoff()


# Thread for handling drone commands
def command_thread_function():
    global is_running
    try:
        tello.takeoff()
        tello.move_forward(100)
        tello.rotate_counter_clockwise(90)
        tello.move_forward(100)
        tello.rotate_counter_clockwise(90)
        tello.move_forward(100)
        tello.rotate_counter_clockwise(90)
        tello.move_forward(100)
        tello.rotate_counter_clockwise(90)
    except Exception as e:
        print(f"An error occurred in the command thread: {e}")
    finally:
        tello.land()
        is_running = False


# --- Main Program Execution ---
if __name__ == "__main__":
    # Initialize Tello object
    tello = Tello()
    tello.connect()
    print("Battery:", tello.get_battery(), "%")

    # Create and start the threads
    video_thread = threading.Thread(target=video_read_thread, daemon=True)
    command_thread = threading.Thread(target=command_thread_function)

    video_thread.start()
    command_thread.start()

    try:
        while is_running:
            # Display the video frame in the main thread
            frame_to_display = None
            with frame_lock:
                frame_to_display = latest_frame

            if frame_to_display is not None:
                # Perform YOLO object detection on the frame.
                # 'stream=True' is recommended for video processing.
                results = model.track(frame_to_display, persist=True, show=False, verbose=False)

                # Get the annotated frame from the results
                # `results[0].plot()` returns the frame with bounding boxes and labels drawn on it.
                annotated_frame = results[0].plot()

                # The `plot()` method already handles the color space,
                # so we no longer need the cvtColor conversion.
                annotated_frame = cv2.resize(annotated_frame, (960, 720))
                cv2.imshow("Tello Video", annotated_frame)

            # Check for keyboard 'q' press to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                is_running = False

    finally:
        command_thread.join()
        video_thread.join(timeout=1)
        cv2.destroyAllWindows()
        tello.end()
        print("Program ended safely.")

