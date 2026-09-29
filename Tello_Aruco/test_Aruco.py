"""
IDEAL Fall 2026 - ArUco Marker Control (threaded)

Learning objectives:
- Read frames from the Tello camera in a background thread
- Detect ArUco markers with OpenCV
- Turn a marker ID into a drone command
- Send drone commands from a separate thread so the video never freezes

Marker IDs (dictionary DICT_4X4_50):
    0 -> land and end the program
    1 -> flip forward
    2 -> flip back
    3 -> flip left
    4 -> flip right

Before flying, run test_Aruco_no_fly.py to check that everything works.
Press Q in the video window to land and quit.
"""

import threading
import time

import cv2
from djitellopy import Tello

# --- Settings you can change ---
COMMAND_COOLDOWN = 3.0    # Seconds to wait after a flip before another flip is allowed
KEEPALIVE_INTERVAL = 5.0  # Seconds between "I'm still here" messages while hovering
MIN_FLIP_BATTERY = 50     # The Tello refuses flips when the battery is at or below about 50%

# Which command each marker ID stands for
MARKER_COMMANDS = {
    0: "LAND",
    1: "FLIP_FORWARD",
    2: "FLIP_BACK",
    3: "FLIP_LEFT",
    4: "FLIP_RIGHT",
}

# --- Shared variables (used by more than one thread) ---
frame_lock = threading.Lock()
latest_frame = None      # Newest camera frame (BGR)
command_lock = threading.Lock()
pending_command = None   # Command the main program wants the drone to do next
is_running = True        # Set to False to stop every thread
in_flight = False


def video_read_thread():
    """Keep copying the newest Tello frame into latest_frame."""
    global latest_frame
    frame_read = tello.get_frame_read()
    while is_running:
        frame = frame_read.frame
        if frame is not None:
            # djitellopy gives RGB frames, but OpenCV expects BGR.
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            with frame_lock:
                latest_frame = frame
        time.sleep(0.01)


def run_command(command):
    """Send one command to the drone. This waits until the drone has finished."""
    if command == "FLIP_FORWARD":
        tello.flip_forward()
    elif command == "FLIP_BACK":
        tello.flip_back()
    elif command == "FLIP_LEFT":
        tello.flip_left()
    elif command == "FLIP_RIGHT":
        tello.flip_right()


def command_thread():
    """Take off, carry out marker commands, and land at the end."""
    global pending_command, is_running, in_flight
    try:
        # Wait (up to 5 s) for the video, so you can see what the drone sees.
        wait_until = time.time() + 5
        while latest_frame is None and time.time() < wait_until:
            time.sleep(0.1)

        print("Taking off...")
        tello.takeoff()
        in_flight = True
        last_command_time = time.time()
        last_flip_time = 0.0

        while is_running:
            # Take the newest request from the main program (and clear it).
            with command_lock:
                command = pending_command
                pending_command = None

            if command == "LAND":
                print("Marker 0 detected: landing.")
                break

            if command is not None and time.time() - last_flip_time > COMMAND_COOLDOWN:
                print(f"Command: {command}")
                try:
                    run_command(command)
                except Exception as error:
                    # For example, the battery is too low to flip. Keep flying.
                    print(f"Command failed: {error}")
                last_flip_time = time.time()
                last_command_time = time.time()

            elif time.time() - last_command_time > KEEPALIVE_INTERVAL:
                # The Tello lands by itself if it hears nothing for 15 seconds.
                tello.send_rc_control(0, 0, 0, 0)
                last_command_time = time.time()

            time.sleep(0.05)

    except Exception as error:
        print(f"An error occurred in the command thread: {error}")
    finally:
        # Always land, even if something went wrong above.
        try:
            if tello.is_flying:
                tello.land()
        except Exception as error:
            print(f"Landing failed: {error}")
        in_flight = False
        is_running = False  # Tell the main program to stop


# --- Main program ---
if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    battery = tello.get_battery()
    print("Battery:", battery, "%")
    if battery <= MIN_FLIP_BATTERY:
        print("Warning: battery is low. The Tello may refuse to flip. Charge the battery first.")
    tello.streamon()

    # ArUco dictionary and detector
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    detector = cv2.aruco.ArucoDetector(aruco_dict, cv2.aruco.DetectorParameters())

    video_thread = threading.Thread(target=video_read_thread, daemon=True)
    drone_thread = threading.Thread(target=command_thread)
    video_thread.start()
    drone_thread.start()

    try:
        while is_running:
            with frame_lock:
                frame = None if latest_frame is None else latest_frame.copy()

            if frame is not None:
                # Detect markers on a grayscale copy of the frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                corners, ids, rejected = detector.detectMarkers(gray)

                if ids is not None:
                    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

                    # ids looks like [[3], [1]] when two markers are visible.
                    # We only use the first marker that was found.
                    marker_id = int(ids[0])
                    command = MARKER_COMMANDS.get(marker_id)
                    if command is not None:
                        # Hand the command to the command thread. The main
                        # program never waits for the drone, so the video
                        # keeps updating while the drone flips.
                        with command_lock:
                            pending_command = command

                status = "FLYING" if in_flight else "ON GROUND"
                cv2.putText(frame, status, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow("ArUco Marker Detection", frame)

            # Press Q to land and quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                is_running = False

    finally:
        print("Stopping...")
        is_running = False
        drone_thread.join(timeout=15)  # Wait for the drone to land
        video_thread.join(timeout=2)
        cv2.destroyAllWindows()
        tello.end()
        print("Program ended safely.")
