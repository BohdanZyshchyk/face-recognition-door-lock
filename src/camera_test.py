import tkinter as tk
from PIL import Image, ImageTk
import cv2

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GStreamer Pi Camera Live View")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Use GStreamer pipeline
        pipeline = (
            "libcamerasrc ! "
            "video/x-raw,format=RGB,width=640,height=480,framerate=30/1 ! "
            "videoconvert ! "
            "appsink"
        )

        self.cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

        if not self.cap.isOpened():
            raise RuntimeError("❌ Failed to open GStreamer pipeline.")

        self.label = tk.Label(self.root)
        self.label.pack()

        self.update_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            self.label.configure(image=photo)
            self.label.image = photo
        self.root.after(30, self.update_frame)

    def on_close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
