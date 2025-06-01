"""
Mock servo motor class for testing on systems without GPIO support
"""

class ServoMotor:
    def __init__(self):
        print("Mock ServoMotor initialized")
        self.is_locked = True
        
    def setAngle(self, angle):
        print(f"Mock: Setting servo angle to {angle}")
        
    def lockDoor(self):
        self.is_locked = True
        print("Mock: Door Locked")
        
    def unlockDoor(self):
        self.is_locked = False
        print("Mock: Door Unlocked")
        
    def cleanup(self):
        print("Mock: Cleanup called") 