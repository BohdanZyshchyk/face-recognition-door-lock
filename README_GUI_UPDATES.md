# Face Recognition Door Lock - GUI Updates

## Overview
The Face Recognition Door Lock application has been updated with an improved GUI that provides better control over the face recognition system and manual door control.

## New Features

### 1. Control Buttons
The application now includes five control buttons at the top of the main window:

- **Start Recognition** (Green): Enables face recognition processing
- **Stop Recognition** (Red): Disables face recognition processing
- **Open Door** (Blue): Manually unlocks the door
- **Close Door** (Orange): Manually locks the door
- **Admin Panel** (Purple): Placeholder for future admin functionality

### 2. Face Recognition Control
- Face recognition is **disabled by default** when the application starts
- Camera feed is always visible, even when face recognition is disabled
- Press "Start Recognition" to begin face detection and automatic door control
- Press "Stop Recognition" to disable face recognition while keeping the camera feed active

### 3. Manual Door Control
- Use "Open Door" and "Close Door" buttons to manually control the door lock
- These buttons work independently of face recognition status
- Useful for testing the door mechanism or providing manual access

### 4. Status Display
The status bar at the bottom shows real-time information:
- "Camera Ready - Face Recognition Disabled" (default state)
- "Face Recognition Started/Stopped" (when toggling recognition)
- "Face ID Found, Unlocking Door!" (when authorized face detected)
- "No face ID found" (when unrecognized face detected)
- "Door Manually Opened/Closed" (when using manual controls)

## Running the Application

### On Raspberry Pi (with GPIO):
```bash
python src/face_recognizer_tkinter.py
```

### On Windows/Other Systems (for testing):
```bash
python src/face_recognizer_tkinter.py
```
The application will automatically use a mock servo motor when GPIO is not available.

## Technical Changes

### gui_app_tkinter.py
- Added control buttons frame with all button controls
- Added face_recognition_enabled flag to VideoThread
- Modified video capture to support both GStreamer (Raspberry Pi) and standard webcam (Windows)
- Added button callback methods for all controls
- Camera feed always displays, face recognition runs conditionally

### face_recognizer_tkinter.py
- Added automatic fallback to mock servo motor when GPIO is not available
- Improved error handling for cross-platform compatibility

### servo_motor_mock.py (New)
- Mock implementation of ServoMotor class for testing without GPIO
- Prints actions to console instead of controlling physical hardware

## Usage Flow
1. Start the application - camera feed will be visible
2. Press "Start Recognition" when ready to enable face detection
3. Authorized faces will automatically unlock the door
4. Use manual controls as needed for testing or override
5. Press "Stop Recognition" to disable automatic face detection
6. Camera feed remains active until application is closed 