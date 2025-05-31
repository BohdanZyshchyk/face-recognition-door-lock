import sys
import cv2
import tkinter as tk
from tkinter import ttk
import threading
import time
from PIL import Image, ImageTk

class VideoThread(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.daemon = True
        self.running = True
        self.face_recognizer_method = None
        self.servo_motor_object = None
        
    def run(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            return_value, image_frame = cap.read()
            if return_value and self.face_recognizer_method:
                # Run the face detector
                image_frame, result = self.face_recognizer_method(image_frame)
                
                # Update the status based on the result
                self.app.update_status(result)
                
                # Execute the motor control action
                if self.servo_motor_object:
                    if result == True:
                        self.servo_motor_object.unlockDoor()
                    else:
                        self.servo_motor_object.lockDoor()
                
                # Convert image for Tkinter display
                self.app.update_image(image_frame)
            
            time.sleep(0.03)  # ~30 FPS
        cap.release()
    
    def stop(self):
        self.running = False
    
    def setFaceRecognizerMethod(self, face_recognizer_method):
        self.face_recognizer_method = face_recognizer_method
    
    def setServoMotorObject(self, servo_motor_object):
        self.servo_motor_object = servo_motor_object

class TkinterApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Face Recognition Door Lock')
        self.root.geometry('1400x1140')
        
        # Configure the main window
        self.root.configure(bg='black')
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Video display label
        self.video_label = tk.Label(self.main_frame, bg='black')
        self.video_label.pack(pady=(0, 20))
        
        # Status text box (using Entry widget as read-only)
        self.status_var = tk.StringVar()
        self.status_var.set("Nothing here")
        self.status_entry = tk.Entry(
            self.main_frame, 
            textvariable=self.status_var,
            state='readonly',
            justify='center',
            font=('Arial', 14),
            width=50
        )
        self.status_entry.pack(side=tk.BOTTOM, pady=20)
        
        # Initialize video thread
        self.video_thread = VideoThread(self)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def update_image(self, cv_image):
        """Convert OpenCV image to Tkinter PhotoImage and update display"""
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        
        # Resize image to fit display (maintaining aspect ratio)
        height, width = rgb_image.shape[:2]
        max_width = 1380  # Adjust based on window size
        max_height = 900
        
        # Calculate scaling factor
        scale = min(max_width/width, max_height/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize image
        rgb_image = cv2.resize(rgb_image, (new_width, new_height))
        
        # Convert to PIL Image then to PhotoImage
        pil_image = Image.fromarray(rgb_image)
        photo = ImageTk.PhotoImage(pil_image)
        
        # Update label (must be done in main thread)
        self.root.after(0, self._update_image_label, photo)
    
    def _update_image_label(self, photo):
        """Update the image label in the main thread"""
        self.video_label.configure(image=photo)
        self.video_label.image = photo  # Keep a reference
    
    def update_status(self, face_found):
        """Update status text based on face recognition result"""
        if face_found:
            status_text = "Face ID Found, Unlocking Door!"
        else:
            status_text = "No face ID found"
        
        # Update status (must be done in main thread)
        self.root.after(0, self._update_status_text, status_text)
    
    def _update_status_text(self, text):
        """Update the status text in the main thread"""
        self.status_var.set(text)
    
    def attachFaceRecognizerObject(self, face_recognizer_object):
        """Attach the face recognizer object"""
        self.face_recognizer_object = face_recognizer_object
        self.video_thread.setFaceRecognizerMethod(face_recognizer_object.runFaceRecognizer)
    
    def attachServoMotorObject(self, servo_motor_object):
        """Attach the servo motor object"""
        self.servo_motor_object = servo_motor_object
        self.video_thread.setServoMotorObject(servo_motor_object)
    
    def start(self):
        """Start the video thread and run the application"""
        self.video_thread.start()
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        self.video_thread.stop()
        self.root.destroy()

if __name__ == '__main__':
    app = TkinterApplication()
    app.start() 