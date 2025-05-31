from gpiozero import Servo, LED, Device
from gpiozero.pins.lgpio import LGPIOFactory
import time

class ServoMotor:
    def __init__(self):
        # Примусово використовуємо LGPIOFactory (сумісна з Pi 5)
        Device.pin_factory = LGPIOFactory()

        self.servo_pin = 17  # BCM-пін
        self.status_pin = 3  # BCM-пін для світлодіода

        # Ініціалізація серво та світлодіода
        self.servo = Servo(self.servo_pin)
        self.status_led = LED(self.status_pin)

        # Початкове положення — мінімальне
        self.servo.min()

    def setAngle(self, angle):
        # Перетворення кута в діапазон від -1 до 1
        servo_value = (angle / 90.0) - 1
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
        self.servo.close()
        self.status_led.close()
