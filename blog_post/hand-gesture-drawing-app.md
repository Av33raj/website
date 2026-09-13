# Building a Hand-Gesture Drawing App with OpenCV and MediaPipe

**GitHub:** [Av33raj/camera-detection](https://github.com/Av33raj/camera-detection)

## Overview

This project turns a regular webcam into a touchless drawing pad. Using computer vision to track hand landmarks in real time, the app lets you "draw" in mid-air just by moving your index finger, with a simple hand gesture acting as an eraser. It also runs live face detection alongside the hand tracking, so the camera feed highlights both faces and hands at the same time.

No mouse, no touchscreen, no stylus — just your hand and a webcam.

## How It Works

The app is built around three computer vision pieces working together in one video loop:

- **Hand tracking** — Google's MediaPipe `HandLandmarker` model detects up to two hands per frame and returns 21 landmark points per hand (fingertips, knuckles, palm base, etc.), which are drawn as connected skeleton lines over the live feed.
- **Gesture recognition** — rather than using a pre-trained gesture classifier, the app checks the relative *y*-position of specific landmarks to work out finger state:
  - Index finger up + middle finger down → **draw**, tracing a line on a persistent canvas as the fingertip moves.
  - Index finger down + middle finger down → **clear**, wiping the canvas.
  - Any other combination → pen up, nothing is drawn.
- **Face detection** — a Haar cascade classifier (`haarcascade_frontalface_default.xml`) runs on each frame in parallel and draws a bounding box around any detected faces.

The drawing itself is kept on a separate canvas (a NumPy array the same size as the frame) rather than drawn directly onto the webcam image. Each frame, that canvas is composited on top of the live video with `cv2.add()`, so the drawing persists across frames instead of being wiped every time a new frame comes in.

## Tech Stack

- **Python**
- **OpenCV** — video capture, face detection, drawing primitives, and display window
- **MediaPipe Tasks (Vision)** — `HandLandmarker` for real-time hand landmark detection
- **NumPy** — the persistent drawing canvas

## Key Implementation Details

Getting gesture-based drawing to feel natural came down to a few things:

- **Frame-accurate video mode** — the `HandLandmarker` is configured with `RunningMode.VIDEO` and fed a timestamp on every call (`cap.get(cv2.CAP_PROP_POS_MSEC)`), which lets MediaPipe use temporal information to track hands more smoothly than treating every frame as an isolated image.
- **Landmark math instead of a gesture model** — comparing the `y` coordinate of a fingertip landmark against its lower knuckle (e.g. index tip vs. index PIP joint) is enough to tell whether a finger is extended or curled, without needing a separate trained classifier.
- **Line continuity** — the app tracks the previous fingertip position (`prev_x`, `prev_y`) and draws a line segment from the last point to the current one each frame, rather than plotting single dots. This is what makes the drawing look like a continuous stroke instead of a dotted trail. The previous point resets to `None` whenever the draw gesture stops, so lifting your finger doesn't join unrelated strokes together.
- **Mirrored view** — the frame is flipped horizontally (`cv2.flip`) so the feed behaves like a mirror, which makes hand movement feel intuitive rather than reversed.

## What I'd Improve Next

- Swap the fixed y-position gesture checks for a small trained gesture classifier to support more gestures (e.g. colour switching, undo).
- Add colour selection and brush size controls, likely via more finger-position gestures or an on-screen menu.
- Replace the Haar cascade face detector with a MediaPipe face detector for better accuracy and to keep the whole pipeline on one library.

## Takeaways

This was a great hands-on (no pun intended) introduction to real-time computer vision — combining a pre-trained landmark model with simple geometric logic to build an interactive feature, rather than needing to train anything from scratch. It's a good example of how far you can get with careful use of existing models plus a bit of coordinate geometry.
