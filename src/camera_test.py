import tkinter as tk
from PIL import Image, ImageTk
from picamera2 import Picamera2

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Camera Live View")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = (640, 480)
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.configure("preview")
        self.picam2.start()

        self.label = tk.Label(self.root)
        self.label.pack()

        self.update_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame(self):
        frame = self.picam2.capture_array()
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)

        self.label.configure(image=photo)
        self.label.image = photo
        self.root.after(30, self.update_frame)

    def on_close(self):
        self.picam2.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
