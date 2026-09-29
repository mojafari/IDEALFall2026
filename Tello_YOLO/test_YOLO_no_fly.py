"""
IDEAL Fall 2026 - YOLO NO-FLY Test (pre-flight check)

Run this BEFORE test_sim_cam_sqv1_YOLO.py. The drone NEVER takes off.
It checks, one step at a time, everything the flying program needs:

    Step 1  Python packages are installed (including "lap", needed for tracking)
    Step 2  The YOLO model file is here and it can detect and track objects
    Step 3  The computer can talk to the Tello, and the battery is charged
    Step 4  The Tello video stream works
    Step 5  Live rehearsal: the same threads as the flying program run.
            YOLO labels the live video while a pretend command thread
            "flies" the square (it only prints the commands). Watch that
            the video keeps moving while the commands run.

During Step 5, walk in front of the camera and hold up everyday objects
(a bottle, a cup, a phone, a backpack), then press Q.
A summary tells you whether you are ready to fly.

Tip: set USE_WEBCAM = True to practice with your laptop webcam (no drone needed).
"""

import sys
import threading
import time
from pathlib import Path

# --- Settings you can change ---
USE_WEBCAM = False        # True = use the laptop webcam instead of the Tello
MODEL_NAME = "yolov8n.pt" # Same model as test_sim_cam_sqv1_YOLO.py
SIDE_LENGTH_CM = 100      # Same square as the flying program
NUMBER_OF_SIDES = 4
MIN_BATTERY = 30          # Do not fly below this
MIN_GOOD_FPS = 5          # Below this, the video will look choppy

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
        print("READY TO FLY: you can now run test_sim_cam_sqv1_YOLO.py")


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
    report("FAIL", "OpenCV installed", "run: pip install -r Tello_YOLO/requirements.txt")
    stop_test()

try:
    import ultralytics
    from ultralytics import YOLO
    report("PASS", "Ultralytics (YOLO) installed", ultralytics.__version__)
except ImportError:
    report("FAIL", "Ultralytics (YOLO) installed", "run: pip install -r Tello_YOLO/requirements.txt")
    stop_test()

try:
    import lap  # noqa: F401  (used by YOLO's object tracker)
    report("PASS", "lap installed", "needed by model.track()")
except ImportError:
    # Without lap, Ultralytics tries to install it during the flight,
    # which fails on the Tello Wi-Fi (no internet).
    report("FAIL", "lap installed", "run: pip install lap  (while on normal internet)")
    stop_test()

try:
    from djitellopy import Tello
    report("PASS", "djitellopy installed")
except ImportError:
    report("FAIL", "djitellopy installed", "run: pip install -r Tello_YOLO/requirements.txt")
    stop_test()

# ----------------------------------------------------------------------
# Step 2: YOLO model
# ----------------------------------------------------------------------
print("\nStep 2: YOLO model")
if Path(MODEL_NAME).exists():
    report("PASS", "Model file found", MODEL_NAME)
else:
    report("INFO", "Model file missing", "YOLO will try to download it now (needs normal internet)")

try:
    model = YOLO(MODEL_NAME)
    report("PASS", "YOLO model loaded", MODEL_NAME)
except Exception as error:
    report("FAIL", "YOLO model loaded",
           f"delete any broken {MODEL_NAME}, connect to normal internet, and run this test again")
    print(f"        details: {error}")
    stop_test()

# Self-test 1: detect objects in a sample photo that comes with Ultralytics.
sample_photo = None
try:
    from ultralytics.utils import ASSETS
    if (ASSETS / "bus.jpg").exists():
        sample_photo = cv2.imread(str(ASSETS / "bus.jpg"))
except ImportError:
    pass

if sample_photo is not None:
    start = time.time()
    sample_result = model.predict(sample_photo, verbose=False)[0]
    predict_ms = (time.time() - start) * 1000
    found = sorted({model.names[int(c)] for c in sample_result.boxes.cls})
    if found:
        report("PASS", "YOLO detects objects", f"found {found} in a sample photo ({predict_ms:.0f} ms)")
    else:
        report("FAIL", "YOLO detects objects", "found nothing in the sample photo")
        stop_test()
else:
    report("INFO", "YOLO detects objects", "sample photo not available, skipped")

# Self-test 2: tracking (this is the part that needs "lap").
try:
    model.track(np.zeros((480, 640, 3), dtype=np.uint8), persist=True, verbose=False)
    report("PASS", "YOLO tracking works")
except Exception as error:
    report("FAIL", "YOLO tracking works", "run: pip install lap  (while on normal internet)")
    print(f"        details: {error}")
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
print("  Walk in front of the camera and hold up everyday objects. Press Q when done.")

frame_lock = threading.Lock()
latest_frame = None
is_running = True
frames_read = 0
current_step = "-"          # Pretend flight step, shown on the screen
flight_plan_finished = False


def video_read_thread():
    """Same job as in the flying program: keep saving the newest frame."""
    global latest_frame, frames_read
    while is_running:
        frame = get_frame()
        if frame is not None:
            with frame_lock:
                latest_frame = frame
                frames_read += 1
        time.sleep(0.01)


def pretend(step, seconds):
    """Print a command and wait about as long as the real drone would take."""
    global current_step
    current_step = step
    print(f"  WOULD SEND: {step}")
    end_time = time.time() + seconds
    while is_running and time.time() < end_time:
        time.sleep(0.05)


def dry_run_command_thread():
    """Same flight plan as the flying program, but it only PRINTS the commands."""
    global current_step, flight_plan_finished
    pretend("takeoff", 3)
    for side in range(NUMBER_OF_SIDES):
        if not is_running:
            return
        pretend(f"move_forward({SIDE_LENGTH_CM})  side {side + 1}", 3)
        pretend(f"rotate_counter_clockwise({360 // NUMBER_OF_SIDES})", 2)
    pretend("land", 2)
    current_step = "flight plan finished - keep testing, press Q when done"
    flight_plan_finished = True


video_thread = threading.Thread(target=video_read_thread, daemon=True)
command_thread = threading.Thread(target=dry_run_command_thread, daemon=True)
video_thread.start()
command_thread.start()

objects_seen = set()
frames_shown = 0
start_time = time.time()

try:
    while is_running:
        with frame_lock:
            frame = None if latest_frame is None else latest_frame.copy()

        if frame is not None:
            results = model.track(frame, persist=True, verbose=False)
            for class_id in results[0].boxes.cls:
                objects_seen.add(model.names[int(class_id)])
            annotated_frame = cv2.resize(results[0].plot(), (960, 720))

            frames_shown += 1
            fps = frames_shown / max(time.time() - start_time, 0.001)
            cv2.putText(annotated_frame, "NO-FLY TEST - drone will not move", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(annotated_frame, f"Would send: {current_step}", (10, 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(annotated_frame, f"FPS: {fps:.0f}", (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("YOLO NO-FLY Test", annotated_frame)

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
    report("WARN", "Detection speed", f"only {fps:.0f} frames per second - close other programs "
                                      "or add imgsz=320 to model.track()")

if objects_seen:
    report("PASS", "Objects detected in live video", ", ".join(sorted(objects_seen)))
else:
    report("WARN", "Objects detected in live video", "none - stand in front of the camera during Step 5")

if flight_plan_finished:
    report("PASS", "Command thread", "pretend flight plan ran while the video kept updating")
else:
    report("WARN", "Command thread", "you stopped before the pretend flight finished (about 25 s)")

print_summary()
