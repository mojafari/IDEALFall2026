# tello_gesture_control.py
import threading
import time
import cv2
from djitellopy import Tello
from gesture_controller import GestureController  # Import the new controller

# Use shared variables for state and communication
frame_lock = threading.Lock()
latest_frame = None
latest_gesture = "HOVER"
is_running = True
command_cooldown = 0.5  # Time in seconds between commands
last_command_time = time.time()
in_flight = False

# --- MediaPipe Setup ---
gesture_controller = GestureController()


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


# Thread for handling drone commands based on gestures
def gesture_command_thread():
    global latest_gesture
    global is_running
    global last_command_time
    global in_flight

    while is_running:
        current_time = time.time()

        # Only send commands if the cooldown period has passed
        if current_time - last_command_time > command_cooldown:
            gesture = latest_gesture
            if gesture == "TAKE_OFF" and not in_flight:
                print("Command: TAKE_OFF")
                tello.takeoff()
                in_flight = True
                last_command_time = current_time
            elif gesture == "LAND" and in_flight:
                print("Command: LAND")
                tello.land()
                in_flight = False
                is_running = False  # End program after landing
                last_command_time = current_time
            elif gesture == "FORWARD" and in_flight:
                print("Command: FORWARD")
                tello.move_forward(30)
                last_command_time = current_time
            elif gesture == "ROTATE_LEFT" and in_flight:
                print("Command: ROTATE_LEFT")
                tello.rotate_counter_clockwise(45)
                last_command_time = current_time
            elif gesture == "HOVER":
                # The drone will naturally hover if no commands are sent.
                pass

        time.sleep(0.1)


# --- Main Program Execution ---
if __name__ == "__main__":
    # Initialize Tello object
    tello = Tello()
    tello.connect()
    print("Battery:", tello.get_battery(), "%")

    # Create and start the threads
    video_thread = threading.Thread(target=video_read_thread, daemon=True)
    command_thread = threading.Thread(target=gesture_command_thread, daemon=True)

    video_thread.start()
    command_thread.start()

    try:
        while is_running:
            # Display the video frame in the main thread
            frame_to_display = None
            with frame_lock:
                frame_to_display = latest_frame

            if frame_to_display is not None:
                # Process the frame for gestures
                gesture, hand_landmarks_list, results = gesture_controller.process_frame(frame_to_display)
                latest_gesture = gesture  # Update the shared gesture state

                # Draw hand landmarks on the frame
                if hand_landmarks_list:
                    for hand_landmarks in hand_landmarks_list:
                        gesture_controller.mp_drawing.draw_landmarks(
                            frame_to_display,
                            hand_landmarks,
                            gesture_controller.mp_hands.HAND_CONNECTIONS
                        )

                # Display the current gesture
                cv2.putText(
                    frame_to_display,
                    f'Gesture: {latest_gesture}',
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA
                )

                # Resize and show the frame
                annotated_frame = cv2.resize(frame_to_display, (960, 720))
                cv2.imshow("Tello Gesture Control", annotated_frame)

            # Check for keyboard 'q' press to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                is_running = False

    finally:
        print("Waiting for threads to join...")
        video_thread.join(timeout=2)
        command_thread.join(timeout=2)
        cv2.destroyAllWindows()
        tello.end()
        print("Program ended safely.")
