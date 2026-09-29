# Fall 2025 Student Project – Group 2: Find the Right Door

This is the work of a Fall 2025 student group, kept as an example. The drone plays a **search mission**: QR codes are taped on several "doors" around the drone, and the drone must turn until it finds the correct one.

## What It Does

1. The drone takes off.
2. When it reads the QR code of a wrong door, it rotates 60° clockwise to look at the next door.
3. When it reads the QR code of the correct door, it lands and the program ends.

The program uses separate threads for the video, the drone commands, and the display, so the video stays smooth while the drone is turning.

## Files

| File | Purpose |
| :--- | :--- |
| `test_Group2.py` | The door-search mission. |
| `test_Group2_qr_gen.py` | Generates the door QR codes as PDFs (`Door 1` to `Door 4` and `Door_Stop`). |

## QR Codes Used

| QR code text | What the code does |
| :---: | :--- |
| `Door 1` | Correct door: land and end the program |
| `Door 2` | Wrong door: rotate 60° clockwise |
| `Door 3` | Wrong door: rotate 60° clockwise |
| Anything else (`Door 4`, `Door_Stop`) | Printed as an unknown door; the drone does nothing |

## Run It

Set up and connect exactly as described in the [main QR code README](../README.md#setup). From this folder, first generate and print the door codes:

```sh
python test_Group2_qr_gen.py
```

Tape the doors about 60° apart around the drone, at the height the drone will hover. Then connect to the Tello Wi‑Fi and run:

```sh
python test_Group2.py
```

Press **Q** to land and quit.

## Things to Notice (Good Discussion or Debugging Exercises)

1. When the drone finds `Door 1`, the message says "QR code 'stop' detected". What should it say instead?
2. The generator makes `Door 4` and `Door_Stop` codes, but the mission program does not use them. How would you add them?
3. The drone only turns when it sees a wrong door. What happens if it is facing a blank wall? How could you make it keep turning until it finds any door?
4. If no command is sent for 15 seconds, the Tello lands by itself. Where in the program could you send a small "keep hovering" command?
5. The video colors look wrong (blue and red are swapped). Find the line in [`test_QRCode.py`](../test_QRCode.py) that fixes this and add it here.
