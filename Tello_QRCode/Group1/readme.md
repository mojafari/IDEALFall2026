# Fall 2025 Student Project – Group 1: Threaded QR Code Control

This is the work of a Fall 2025 student group, kept as an example. It extends [`test_QRCode.py`](../test_QRCode.py) by moving QR detection into its own **thread**.

## What It Does

The program uses three parts that run at the same time:

| Part | Job |
| :--- | :--- |
| `video_read_thread` | Keeps saving the newest camera frame. |
| `qr_detection_thread` | Looks for QR codes in the newest frame and sends drone commands. |
| Main program | Shows the video window and watches for the **Q** key. |

Because the drone commands run in a separate thread, the video window keeps updating even while the drone is flipping.

## QR Codes Used

| QR code text | What the code does |
| :---: | :--- |
| `stop` | Land and end the program |
| `up` | Flip forward |
| `down` | Flip back |
| `flip_left` | Flip left |
| `flip_right` | Flip right |

Generate these with the [QR code generator](../QRCode_Generator/README.md) by changing its `commands` dictionary.

## Run It

Set up and connect exactly as described in the [main QR code README](../README.md#setup), then run from this folder:

```sh
python test_group1.py
```

The drone takes off automatically. Press **Q** to land and quit.

## Things to Notice (Good Discussion or Debugging Exercises)

1. The QR code `up` makes the drone **flip forward**, and `down` makes it **flip back**. The printed messages also say "flip_forward" and "flip_back". What would you rename to make the program easier to understand?
2. There is no cooldown. What happens if the `up` code stays in front of the camera? Compare with how [`test_QRCode.py`](../test_QRCode.py) handles this.
3. The video colors look wrong (blue and red are swapped). Find the line in [`test_QRCode.py`](../test_QRCode.py) that fixes this and add it to this program.
4. If no command is sent for 15 seconds, the Tello lands by itself. How could the program keep the drone flying while it waits for a QR code?
