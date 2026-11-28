"""Try the pre-trained YOLO11n ASL letter model on your webcam.

Run natively (not in Docker, which can't reach the Mac camera):
    pipenv run python try_yolo.py

Press q to quit. Press s to save the current frame to snapshots/ for testing.
Model: https://huggingface.co/ajdanoff/asl-unified-letters-yolo11n-mp (MIT)
"""

import time
from pathlib import Path

import cv2
from ultralytics import YOLO

MODEL_PATH = Path(__file__).parent / "models" / "asl_letters_yolo11n.pt"
SNAPSHOT_DIR = Path(__file__).parent / "snapshots"
CONFIDENCE = 0.5  # the model card's example uses 0.7; lower shows more guesses
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)


def draw_results(frame, result, names, elapsed_ms):
    """Draw each detected letter's box and label, plus the frame time."""
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = f"{names[int(box.cls)]} {float(box.conf):.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), GREEN, 2)
        cv2.putText(
            frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, GREEN, 2
        )
    cv2.putText(
        frame,
        f"{elapsed_ms:.0f} ms/frame",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        WHITE,
        2,
    )


def save_snapshot(frame):
    """Save the current frame so it can be reused as a test image."""
    SNAPSHOT_DIR.mkdir(exist_ok=True)
    path = SNAPSHOT_DIR / f"frame_{int(time.time() * 1000)}.jpg"
    cv2.imwrite(str(path), frame)
    print("saved", path)


def main():
    """Open the webcam, run the model on each frame, and show the results."""
    model = YOLO(str(MODEL_PATH))
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise SystemExit(
            "Could not open the webcam. On macOS, allow camera access for your "
            "terminal or VS Code in System Settings > Privacy & Security > Camera."
        )

    while True:
        ok, frame = camera.read()
        if not ok:
            break
        frame = cv2.flip(frame, 1)  # mirror view, like a selfie camera

        start = time.perf_counter()
        results = model(frame, imgsz=512, conf=CONFIDENCE, device="cpu", verbose=False)
        draw_results(
            frame, results[0], model.names, (time.perf_counter() - start) * 1000
        )
        cv2.imshow("ASL YOLO test (q = quit, s = save frame)", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("s"):
            save_snapshot(frame)

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
