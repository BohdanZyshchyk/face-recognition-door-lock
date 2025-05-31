from gpiozero import Servo, LED
from gpiozero.pins.pigpio import PiGPIOFactory
import time

class ServoMotor:
    def __init__(self):
        try:
            # Try to use pigpio for better PWM control
            factory = PiGPIOFactory()
        except:
            # Fallback to default pin factory
            factory = None
            
        self.servo_pin = 17
        self.status_pin = 3
        
        # Initialize servo with correction factor for more accurate positioning
        if factory:
            self.servo = Servo(self.servo_pin, pin_factory=factory)
        else:
            self.servo = Servo(self.servo_pin)
            
        self.status_led = LED(self.status_pin)
        
        # Set initial position
        self.servo.min()

    def setAngle(self, angle):
        # Convert angle (0-180) to servo value (-1 to 1)
        # 0 degrees = -1, 90 degrees = 0, 180 degrees = 1
        servo_value = (angle / 90.0) - 1
        
        # Clamp value between -1 and 1
        servo_value = max(-1, min(1, servo_value))
        
        self.status_led.on()
        self.servo.value = servo_value
        time.sleep(1)
        self.status_led.off()

    def lockDoor(self):
        self.setAngle(90)
        print("Door Locked")
    
    def unlockDoor(self):
        self.setAngle(0)
        print("Door Unlocked")
        
    def cleanup(self):
        """Clean up GPIO resources"""
        self.servo.close()
        self.status_led.close()