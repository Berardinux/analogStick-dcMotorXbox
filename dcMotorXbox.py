# DC motor
import RPi.GPIO as GPIO
import time
# Controller
import evdev
import numpy as np

# Motor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
motorSpeed = GPIO.PWM(22, 1000)
motorSpeed.start(0)

# Controller
def map_value(value, in_min, in_max, out_min, out_max):
    return np.interp(value, [in_min, in_max], [out_min, out_max])
device = evdev.InputDevice('/dev/input/event2')
print(device)

# Motor control methods
def forward(speed):
    print(f"Going Forward at {speed}%")
    GPIO.output(16, True)
    GPIO.output(18, False) 
    motorSpeed.ChangeDutyCycle(speed)

def backward(speed):
    print(f"Going Backward at {speed}%")
    GPIO.output(16, False)
    GPIO.output(18, True)
    motorSpeed.ChangeDutyCycle(speed)

try:
    # Event loop
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            # Right Trigger
            if event.code == evdev.ecodes.ABS_GAS:
                speed = round(map_value(event.value, 0, 1023, 0, 100))
                print(f"Right Trigger: {event.value}")
                forward(speed)
            # Left Trigger
            elif event.code == evdev.ecodes.ABS_BRAKE:
                speed = round(map_value(event.value, 0, 1023, 0, 100))
                print(f"Left Trigger: {event.value}")
                backward(speed)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
