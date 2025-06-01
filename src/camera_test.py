import cv2
import gi
import sys

gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(sys.argv[1:])
print("? GStreamer version:", Gst.version_string())

pipeline = (
    "libcamerasrc ! "
    "video/x-raw,format=RGB,width=640,height=480,framerate=30/1 ! "
    "videoconvert ! appsink"
)

cap = cv2.VideoCapture(pipeline)
if not cap.isOpened():
    print("? Failed to open pipeline")
    sys.exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("? Failed to read frame")
        break

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
