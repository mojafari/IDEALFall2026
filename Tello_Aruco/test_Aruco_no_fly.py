"""
IDEAL Fall 2026 - ArUco NO-FLY Test (pre-flight check)

Run this BEFORE test_Aruco.py. The drone NEVER takes off.
It checks, one step at a time, everything the flying program needs:

    Step 1  Python packages are installed
    Step 2  The ArUco detector works (tested on a marker drawn by the computer)
    Step 3  The computer can talk to the Tello, and the battery is charged
    Step 4  The Tello video stream works
    Step 5  Live rehearsal: the same threads as the flying program run,
            markers are detected, and the command that WOULD be sent is
            shown. Nothing is sent to the drone.

During Step 5, hold each printed marker (IDs 0-4) in front of the camera,
then press Q. A summary tells you whether you are ready to fly.

Tip: set USE_WEBCAM = True to practice with your laptop webcam (no drone needed).
"""

import sys
import threading
import time

# --- Settings you can change ---
USE_WEBCAM = False       # True = use the laptop webcam instead of the Tello
COMMAND_COOLDOWN = 3.0   # Same cooldown as test_Aruco.py
MIN_FLIP_BATTERY = 50    # The Tello refuses flips at or below about 50%
MIN_GOOD_FPS = 10        # Below this, the video is too slow for smooth control

MARKER_COMMANDS = {      # Same table as test_Aruco.py
    0: "LAND",
    1: "FLIP_FORWARD",
    2: "FLIP_BACK",
    3: "FLIP_LEFT",
    4: "FLIP_RIGHT",
}

# ----------------------------------------------------------------------
# Reporting helpers
# ----------------------------------------------------------------------
checks = []  # (status, name, detail) for the summary at the end


def report(status, name, detail=""):
    """Record and print one check. status is PASS, WARN, FAIL, or INFO."""
    checks.append((status, name, detail))
    print(f"  [{status}] {name}" + (f" - {detail}" if detail else ""))


def print_summary():
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for status, name, detail in checks:
        print(f"  [{status}] {name}" + (f" - {detail}" if detail else ""))
    statuses = [status for status, _, _ in checks]
    print()
    if "FAIL" in statuses:
        print("NOT READY: fix the FAIL items above, then run this test again.")
    elif "WARN" in statuses:
        print("READY WITH WARNINGS: read the WARN items before you fly.")
    else:
        print("READY TO FLY: you can now run test_Aruco.py")


def stop_test():
    """Stop early after a FAIL that makes the next steps impossible."""
    print_summary()
    sys.exit(1)


# ----------------------------------------------------------------------
# Step 1: Python packages
# ----------------------------------------------------------------------
print("\nStep 1: Python packages")
try:
    import cv2
    report("PASS", "OpenCV installed", cv2.__version__)
except ImportError:
    report("FAIL", "OpenCV installed", "run: pip install -r Tello_Aruco/requirements.txt")
    stop_test()

try:
    from djitellopy import Tello
    report("PASS", "djitellopy installed")
except ImportError:
    report("FAIL", "djitellopy installed", "run: pip install -r Tello_Aruco/requirements.txt")
    stop_test()

# ----------------------------------------------------------------------
# Step 2: Detector self-test
# ----------------------------------------------------------------------
print("\nStep 2: ArUco detector")
if not hasattr(cv2, "aruco") or not hasattr(cv2.aruco, "ArucoDetector"):
    report("FAIL", "ArUco detector available", "OpenCV 4.7 or newer is needed: pip install --upgrade opencv-python")
    stop_test()

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(aruco_dict, cv2.aruco.DetectorParameters())

# Self-test: let the computer draw marker 1, then try to detect it.
test_marker = cv2.aruco.generateImageMarker(aruco_dict, 1, 200)
test_image = cv2.copyMakeBorder(test_marker, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=255)
_, test_ids, _ = detector.detectMarkers(test_image)
print(test_ids)
if test_ids is not None and int(test_ids[0]) == 1:
    report("PASS", "ArUco detector works", "found marker 1 in a test image")
else:
    report("FAIL", "ArUco detector works", "could not find a marker in a perfect test image")
    stop_test()

# ----------------------------------------------------------------------
# Step 3: Drone connection and battery
# ----------------------------------------------------------------------
print("\nStep 3: Drone connection")
tello = None
if USE_WEBCAM:
    report("INFO", "Drone connection", "skipped because USE_WEBCAM = True")
else:
    tello = Tello()
    try:
        tello.connect()
        report("PASS", "Connected to the Tello")
    except Exception:
        report("FAIL", "Connected to the Tello",
               "is the drone on, and is this computer on the TELLO-XXXXXX Wi-Fi?")
        stop_test()

    battery = tello.get_battery()
    if battery > MIN_FLIP_BATTERY:
        report("PASS", "Battery", f"{battery}%")
    elif battery > 20:
        report("WARN", "Battery", f"{battery}% - flips need more than {MIN_FLIP_BATTERY}%, charge it")
    else:
        report("FAIL", "Battery", f"{battery}% - too low to fly")

# ----------------------------------------------------------------------
# Step 4: Video stream
# ----------------------------------------------------------------------
print("\nStep 4: Video stream")
camera = None
if USE_WEBCAM:
    camera = cv2.VideoCapture(0)

    def get_frame():
        ok, frame = camera.read()   # webcam frames are already BGR
        return frame if ok else None
else:
    tello.streamon()
    frame_read = tello.get_frame_read()

    def get_frame():
        frame = frame_read.frame
        if frame is None:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Tello frames are RGB

# The first Tello frames are completely black, so wait for a real picture.
first_frame = None
wait_until = time.time() + 10
while time.time() < wait_until:
    frame = get_frame()
    if frame is not None and frame.max() > 0:
        first_frame = frame
        break
    time.sleep(0.1)

if first_frame is None:
    report("FAIL", "Video stream", "no picture after 10 seconds")
    if tello is not None:
        tello.end()
    stop_test()
height, width = first_frame.shape[:2]
report("PASS", "Video stream", f"{width} x {height} pixels")

# ----------------------------------------------------------------------
# Step 5: Live rehearsal with the same threads as the flying program
# ----------------------------------------------------------------------
print("\nStep 5: Live rehearsal (the drone will NOT move)")
print("  Hold markers 0-4 in front of the camera, one at a time. Press Q when done.")

frame_lock = threading.Lock()
latest_frame = None
command_lock = threading.Lock()
pending_command = None
is_running = True
frames_read = 0
commands_would_send = []   # Every command the command thread would have sent
last_would_send = "-"      # Shown on the screen


def video_read_thread():
    """Same job as in test_Aruco.py: keep saving the newest frame."""
    global latest_frame, frames_read
    while is_running:
        frame = get_frame()
        if frame is not None:
            with frame_lock:
                latest_frame = frame
                frames_read += 1
        time.sleep(0.01)


def dry_run_command_thread():
    """Same logic as test_Aruco.py, but it only PRINTS the commands."""
    global pending_command, last_would_send
    last_flip_time = 0.0
    while is_running:
        with command_lock:
            command = pending_command
            pending_command = None

        if command == "LAND":
            if last_would_send != "LAND":
                print("  WOULD SEND: LAND (and the flying program would end)")
                commands_would_send.append(command)
                last_would_send = "LAND"
        elif command is not None and time.time() - last_flip_time > COMMAND_COOLDOWN:
            print(f"  WOULD SEND: {command}")
            commands_would_send.append(command)
            last_would_send = command
            last_flip_time = time.time()
        time.sleep(0.05)


video_thread = threading.Thread(target=video_read_thread, daemon=True)
command_thread = threading.Thread(target=dry_run_command_thread, daemon=True)
video_thread.start()
command_thread.start()

markers_seen = set()
frames_shown = 0
start_time = time.time()

try:
    while is_running:
        with frame_lock:
            frame = None if latest_frame is None else latest_frame.copy()

        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejected = detector.detectMarkers(gray)
            if ids is not None:
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                marker_id = int(ids[0])
                markers_seen.add(marker_id)
                command = MARKER_COMMANDS.get(marker_id)
                if command is not None:
                    with command_lock:
                        pending_command = command

            frames_shown += 1
            fps = frames_shown / max(time.time() - start_time, 0.001)
            cv2.putText(frame, "NO-FLY TEST - drone will not move", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Would send: {last_would_send}", (10, 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Markers seen: {sorted(markers_seen)}   FPS: {fps:.0f}", (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("ArUco NO-FLY Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            is_running = False

finally:
    is_running = False
    video_thread.join(timeout=2)
    command_thread.join(timeout=2)
    cv2.destroyAllWindows()
    if camera is not None:
        camera.release()
    if tello is not None:
        tello.streamoff()
        tello.end()

# ----------------------------------------------------------------------
# Results of the live rehearsal
# ----------------------------------------------------------------------
elapsed = max(time.time() - start_time, 0.001)
fps = frames_shown / elapsed
if frames_read > 0:
    report("PASS", "Video thread", f"{frames_read} frames received")
else:
    report("FAIL", "Video thread", "no frames were received during the rehearsal")

if fps >= MIN_GOOD_FPS:
    report("PASS", "Detection speed", f"{fps:.0f} frames per second")
else:
    report("WARN", "Detection speed", f"only {fps:.0f} frames per second - close other programs")

for marker_id, command in MARKER_COMMANDS.items():
    if marker_id in markers_seen:
        report("PASS", f"Marker {marker_id} ({command})", "detected")
    else:
        report("WARN", f"Marker {marker_id} ({command})", "not tested - show it during Step 5")

if commands_would_send:
    report("PASS", "Command thread", f"would have sent {len(commands_would_send)} command(s)")
else:
    report("WARN", "Command thread", "no commands were triggered - show a marker during Step 5")

print_summary()
