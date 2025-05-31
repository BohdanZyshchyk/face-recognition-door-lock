from servo_motor import ServoMotor
from face_recognizer_tkinter import FaceRecognizer

class FaceRecognitionDoorLock:
	def __init__(self):
		self.servo_motor = ServoMotor()
		self.face_recognizer = self.initializeFaceRecognitionEngine()

	def initializeFaceRecognitionEngine(self):
		"""Initialize the face recognition engine"""
		return FaceRecognizer()




