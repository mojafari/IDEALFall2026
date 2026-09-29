"""
IDEAL Fall 2026 - Gesture Control NO-FLY Test (pre-flight check)

Run this BEFORE tello_gesture_control.py. The drone NEVER takes off.
It checks, one step at a time, everything the flying program needs:

    Step 1  Python packages are installed (including the new MediaPipe Tasks API)
    Step 2  The hand model file is here and MediaPipe can run it
    Step 3  The computer can talk to the Tello, and the battery is charged
    Step 4  The Tello video stream works
    Step 5  Live rehearsal: the same threads and safety rules as the flying
            program run, and the command that WOULD be sent is shown.
            Nothing is sent to the drone.

During Step 5, show every gesture to the drone's camera, then press Q.
A summary tells you whether you are ready to fly.

Tip: set USE_WEBCAM = True to practice with your laptop webcam (no drone needed).
"""

import sys
import threading
import time

# --- Settings you can change ---
USE_WEBCAM = False       # True = use the laptop webcam instead of the Tello
HOLD_TIME = 0.3          # Same settings as tello_gesture_control.py
COMMAND_COOLDOWN = 0.5
MIN_BATTERY = 30         # Do not fly below this
MIN_GOOD_FPS = 10        # Below this, gestures will feel slow to respond

ALL_GESTURES = ["TAKE_OFF", "FORWARD", "ROTATE_LEFT", "HOVER", "LAND"]

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
        print("READY TO FLY: you can now run tello_gesture_control.py")


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
    import numpy as np
    report("PASS", "OpenCV installed", cv2.__version__)
except ImportError:
    report("FAIL", "OpenCV installed", "run: pip install -r Tello_GestureCTRL/requirements.txt")
    stop_test()

try:
    import mediapipe as mp
    from mediapipe.tasks.python import vision  # noqa: F401  (the new Tasks API)
    report("PASS", "MediaPipe installed", f"{mp.__version__} (Tasks API available)")
except ImportError:
    report("FAIL", "MediaPipe installed",
           "run: pip install -r Tello_GestureCTRL/requirements.txt  (if pip cannot find "
           "mediapipe, your Python is too new; use Python 3.12)")
    stop_test()

try:
    from djitellopy import Tello
    report("PASS", "djitellopy installed")
except ImportError:
    report("FAIL", "djitellopy installed", "run: pip install -r Tello_GestureCTRL/requirements.txt")
    stop_test()

# ----------------------------------------------------------------------
# Step 2: Hand model
# ----------------------------------------------------------------------
print("\nStep 2: Hand model")
from gesture_controller import MODEL_PATH, GestureController

if MODEL_PATH.exists():
    report("PASS", "Model file found", MODEL_PATH.name)
else:
    report("INFO", "Model file missing", "trying to download it now (needs normal internet)")

try:
    gesture_controller = GestureController()   # downloads the model if needed
except Exception as error:
    report("FAIL", "Hand model loaded",
           "connect to normal internet (not the Tello Wi-Fi) and run: python gesture_controller.py")
    print(f"        details: {error}")
    stop_test()

# Self-test: an empty gray picture must give "NO_HAND", and we time the model.
test_image = np.full((720, 960, 3), 128, dtype=np.uint8)
start = time.time()
test_gesture, _ = gesture_controller.process_frame(test_image)
model_ms = (time.time() - start) * 1000
if test_gesture == "NO_HAND":
    report("PASS", "Hand model runs", f"{model_ms:.0f} ms for one frame (first frame is always slowest)")
else:
    report("FAIL", "Hand model runs", f"found '{test_gesture}' in an empty picture")
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
    if battery >= MIN_BATTERY:
        report("PASS", "Battery", f"{battery}%")
    else:
        report("FAIL", "Battery", f"{battery}% - charge it to at least {MIN_BATTERY}% before flying")

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
print("  Show each gesture: open hand, index finger, peace sign, relaxed hand, fist.")
print("  Press Q when done.")

frame_lock = threading.Lock()
latest_frame = None
active_gesture = "NO_HAND"
is_running = True
pretend_in_flight = False   # The rehearsal pretends to take off and land
frames_read = 0
commands_would_send = []
last_would_send = "-"


def video_read_thread():
    """Same job as in tello_gesture_control.py: keep saving the newest frame."""
    global latest_frame, frames_read
    while is_running:
        frame = get_frame()
        if frame is not None:
            with frame_lock:
                latest_frame = frame
                frames_read += 1
        time.sleep(0.01)


def would_send(text):
    global last_would_send
    print(f"  WOULD SEND: {text}")
    commands_would_send.append(text)
    last_would_send = text


def dry_run_command_thread():
    """Same rules as tello_gesture_control.py, but it only PRINTS the commands."""
    global pretend_in_flight
    last_command_time = time.time()
    ready_for_move = True
    while is_running:
        gesture = active_gesture
        if gesture in ("HOVER", "NO_HAND"):
            ready_for_move = True

        if time.time() - last_command_time > COMMAND_COOLDOWN:
            if gesture == "TAKE_OFF" and not pretend_in_flight:
                would_send("takeoff")
                pretend_in_flight = True
                ready_for_move = False
                last_command_time = time.time()
            elif gesture == "LAND" and pretend_in_flight:
                would_send("land  (the flying program would end here)")
                pretend_in_flight = False
                last_command_time = time.time()
            elif gesture == "FORWARD" and pretend_in_flight and ready_for_move:
                would_send("move_forward")
                ready_for_move = False
                last_command_time = time.time()
            elif gesture == "ROTATE_LEFT" and pretend_in_flight and ready_for_move:
                would_send("rotate_counter_clockwise")
                ready_for_move = False
                last_command_time = time.time()
        time.sleep(0.05)


video_thread = threading.Thread(target=video_read_thread, daemon=True)
command_thread = threading.Thread(target=dry_run_command_thread, daemon=True)
video_thread.start()
command_thread.start()

gestures_seen = set()
seen_gesture = "NO_HAND"
seen_since = time.time()
frames_shown = 0
start_time = time.time()

try:
    while is_running:
        with frame_lock:
            frame = None if latest_frame is None else latest_frame.copy()

        if frame is not None:
            gesture, landmarks = gesture_controller.process_frame(frame)

            # Same hold-time rule as the flying program
            now = time.time()
            if gesture != seen_gesture:
                seen_gesture = gesture
                seen_since = now
            if now - seen_since >= HOLD_TIME:
                active_gesture = seen_gesture
                gestures_seen.add(active_gesture)

            if landmarks is not None:
                gesture_controller.draw_landmarks(frame, landmarks)

            frames_shown += 1
            fps = frames_shown / max(time.time() - start_time, 0.001)
            state = "pretend FLYING" if pretend_in_flight else "pretend ON GROUND"
            cv2.putText(frame, "NO-FLY TEST - drone will not move", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Active: {active_gesture}  ({state})", (10, 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Would send: {last_would_send}", (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"FPS: {fps:.0f}", (10, 135),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("Gesture NO-FLY Test", cv2.resize(frame, (960, 720)))

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
fps = frames_shown / max(time.time() - start_time, 0.001)
if frames_read > 0:
    report("PASS", "Video thread", f"{frames_read} frames received")
else:
    report("FAIL", "Video thread", "no frames were received during the rehearsal")

if fps >= MIN_GOOD_FPS:
    report("PASS", "Detection speed", f"{fps:.0f} frames per second")
else:
    report("WARN", "Detection speed", f"only {fps:.0f} frames per second - close other programs")

for gesture in ALL_GESTURES:
    if gesture in gestures_seen:
        report("PASS", f"Gesture {gesture}", "recognized")
    else:
        report("WARN", f"Gesture {gesture}", "not tested - show it during Step 5")

if commands_would_send:
    report("PASS", "Command thread", f"would have sent {len(commands_would_send)} command(s)")
else:
    report("WARN", "Command thread", "no commands were triggered - start with an open hand")

print_summary()
