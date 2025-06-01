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
        self.face_recognition_enabled = False  # Face recognition is disabled by default
        
    def run(self):
        # Try GStreamer pipeline first (for Raspberry Pi)
        try:
            pipeline = ("libcamerasrc ! "
            "video/x-raw,format=RGB,width=640,height=480,framerate=30/1 ! "
            "videoconvert ! appsink")
            cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
            if not cap.isOpened():
                raise Exception("GStreamer pipeline failed")
        except:
            # Fallback to default camera (for Windows/other platforms)
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                # Try other camera indices
                for i in range(1, 4):
                    cap = cv2.VideoCapture(i)
                    if cap.isOpened():
                        break
        
        while self.running:
            return_value, image_frame = cap.read()
            if return_value:
                # Only run face recognition if enabled and method is available
                if self.face_recognition_enabled and self.face_recognizer_method:
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
                else:
                    # When face recognition is disabled, show default status
                    self.app.update_status(None)
                
                # Always convert and display the image
                self.app.update_image(image_frame)
            
            time.sleep(0.03)  # ~30 FPS
        cap.release()
    
    def stop(self):
        self.running = False
    
    def setFaceRecognizerMethod(self, face_recognizer_method):
        self.face_recognizer_method = face_recognizer_method
    
    def setServoMotorObject(self, servo_motor_object):
        self.servo_motor_object = servo_motor_object
    
    def enableFaceRecognition(self, enable):
        self.face_recognition_enabled = enable

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
        
        # Create control buttons frame at the top
        self.control_frame = tk.Frame(self.main_frame, bg='black')
        self.control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create buttons
        button_style = {'font': ('Arial', 12), 'width': 15, 'height': 2}
        
        self.start_button = tk.Button(
            self.control_frame, 
            text="Start Recognition", 
            command=self.start_recognition,
            bg='green',
            fg='white',
            **button_style
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            self.control_frame, 
            text="Stop Recognition", 
            command=self.stop_recognition,
            bg='red',
            fg='white',
            state='disabled',
            **button_style
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.open_door_button = tk.Button(
            self.control_frame, 
            text="Open Door", 
            command=self.open_door,
            bg='blue',
            fg='white',
            **button_style
        )
        self.open_door_button.pack(side=tk.LEFT, padx=5)
        
        self.close_door_button = tk.Button(
            self.control_frame, 
            text="Close Door", 
            command=self.close_door,
            bg='orange',
            fg='white',
            **button_style
        )
        self.close_door_button.pack(side=tk.LEFT, padx=5)
        
        self.admin_button = tk.Button(
            self.control_frame, 
            text="Admin Panel", 
            command=self.open_admin_panel,
            bg='purple',
            fg='white',
            **button_style
        )
        self.admin_button.pack(side=tk.LEFT, padx=5)
        
        # Video display label
        self.video_label = tk.Label(self.main_frame, bg='black')
        self.video_label.pack(pady=(0, 20))
        
        # Status text box (using Entry widget as read-only)
        self.status_var = tk.StringVar()
        self.status_var.set("Camera Ready - Face Recognition Disabled")
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
        
        # Store references
        self.face_recognizer_object = None
        self.servo_motor_object = None
        
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
        if face_found is None:
            # Face recognition is disabled
            status_text = "Camera Ready - Face Recognition Disabled"
        elif face_found:
            status_text = "Face ID Found, Unlocking Door!"
        else:
            status_text = "No face ID found"
        
        # Update status (must be done in main thread)
        self.root.after(0, self._update_status_text, status_text)
    
    def _update_status_text(self, text):
        """Update the status text in the main thread"""
        self.status_var.set(text)
    
    def start_recognition(self):
        """Start face recognition"""
        self.video_thread.enableFaceRecognition(True)
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_var.set("Face Recognition Started")
    
    def stop_recognition(self):
        """Stop face recognition"""
        self.video_thread.enableFaceRecognition(False)
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Face Recognition Stopped")
    
    def open_door(self):
        """Manually open the door"""
        if self.servo_motor_object:
            self.servo_motor_object.unlockDoor()
            self.status_var.set("Door Manually Opened")
    
    def close_door(self):
        """Manually close the door"""
        if self.servo_motor_object:
            self.servo_motor_object.lockDoor()
            self.status_var.set("Door Manually Closed")
    
    def open_admin_panel(self):
        """Open admin panel (placeholder)"""
        self.status_var.set("Admin Panel - Coming Soon")
    
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
