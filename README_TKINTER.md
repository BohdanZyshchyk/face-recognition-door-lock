# Face Recognition Door Lock - Tkinter Version

Repository to implement a Face Recognition based door lock/unlock system using Raspberry Pi, a CSI camera, and a servo motor with Tkinter GUI.

## Project Overview

This project has been migrated from PyQt5 to Tkinter to provide a more lightweight and native Python GUI solution. The system includes:

- **Real-time face recognition** using the `face_recognition` library
- **Live video feed** displayed in a Tkinter GUI
- **Servo motor control** for door locking/unlocking
- **Status updates** showing recognition results
- **Multi-threading** for smooth video processing

## Architecture

### Components:

1. **`servo_motor.py`** - Controls servo motor for door lock/unlock
2. **`gui_app_tkinter.py`** - Tkinter-based GUI application (replaces PyQt5)
3. **`face_recognizer_tkinter.py`** - Face recognition engine (updated for Tkinter)
4. **`face_recognition_door_lock.py`** - Main application class

### Key Changes from PyQt5 to Tkinter:

| PyQt5 Component | Tkinter Equivalent | Purpose |
|-----------------|-------------------|---------|
| `QApplication` | `tk.Tk()` | Main application window |
| `QWidget` | `tk.Frame` | Container widgets |
| `QLabel` | `tk.Label` | Image and text display |
| `QLineEdit` | `tk.Entry` | Status text (read-only) |
| `QVBoxLayout` | `pack()` layout | Widget positioning |
| `QThread` | `threading.Thread` | Background video processing |
| `QImage/QPixmap` | `PIL.Image/ImageTk.PhotoImage` | Image handling |
| `pyqtSignal/pyqtSlot` | `root.after()` | Thread-safe GUI updates |

## Installation

### Prerequisites:
- Python 3.7+
- Raspberry Pi with camera module
- Servo motor connected to GPIO pin 17

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Required packages:
- `tkinter` (usually comes with Python)
- `opencv-python`
- `face_recognition`
- `Pillow` (PIL)
- `RPi.GPIO` (for Raspberry Pi)
- `numpy`

## Usage

### Setup:
1. Place known face images in the `saved_images/` directory
2. Image files should be named `PERSON_NAME.jpg`
3. Connect servo motor to GPIO pin 17
4. Connect camera to Raspberry Pi

### Run the application:

**Option 1: Run main application**
```bash
python src/face_recognition_door_lock.py
```

**Option 2: Run face recognizer directly**
```bash
python src/face_recognizer_tkinter.py
```

**Option 3: Run GUI only (for testing)**
```bash
python src/gui_app_tkinter.py
```

## Features

### Face Recognition:
- Loads known faces from `saved_images/` directory
- Real-time face detection and recognition
- Bounding box display around detected faces
- Name labels for recognized faces

### GUI:
- Live video feed display (1400x1140 window)
- Status updates ("Face ID Found, Unlocking Door!" / "No face ID found")
- Clean, modern interface with proper aspect ratio scaling
- Thread-safe updates using `root.after()`

### Door Control:
- Automatic door unlock for recognized faces
- Automatic door lock for unknown/no faces
- Servo motor control via GPIO pins
- Status LED indicator (GPIO pin 3)

## Technical Details

### Threading:
- Main GUI runs on primary thread
- Video capture and processing on separate `VideoThread`
- Thread-safe GUI updates using Tkinter's `after()` method

### Image Processing:
- OpenCV for video capture and processing
- PIL (Pillow) for Tkinter image conversion
- Automatic image scaling to fit display
- Frame skipping for performance optimization

### Performance Optimizations:
- Process every 3rd frame for efficiency
- Image scaling (1/3 size) for face recognition
- Proper memory management with image references

## Troubleshooting

### Common Issues:

1. **Camera not found**: Ensure camera is properly connected and enabled
2. **GPIO permission errors**: Run with sudo or add user to gpio group
3. **Import errors**: Install missing dependencies from requirements.txt
4. **Face not recognized**: Ensure good quality images in saved_images/
5. **GUI threading errors**: All GUI updates use `root.after()` for thread safety

### Dependencies:
- Ensure all packages in `requirements.txt` are installed
- For Raspberry Pi: `sudo apt-get install python3-tk` if tkinter is missing
- For face_recognition: May need `cmake` and `dlib` compilation

## Migration Notes

The Tkinter version maintains full compatibility with the original PyQt5 functionality while providing:
- Better native Python integration
- Reduced dependencies (no Qt installation required)
- Simplified deployment
- Cross-platform compatibility
- Lower memory footprint

All original features are preserved including face recognition accuracy, servo motor control, and real-time video processing. 