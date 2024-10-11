# DC motor
import RPi.GPIO as GPIO
import time
# Controller
import evdev
import numpy as np

# Motor GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)  # Direction pin 1
GPIO.setup(18, GPIO.OUT)  # Direction pin 2
GPIO.setup(22, GPIO.OUT)  # PWM pin
motorSpeed = GPIO.PWM(22, 1000)  # Set PWM frequency
motorSpeed.start(0)  # Start with 0% duty cycle

# Controller setup
def map_value(value, in_min, in_max, out_min, out_max):
    return np.interp(value, [in_min, in_max], [out_min, out_max])

device = evdev.InputDevice('/dev/input/event2')  # Adjust if necessary
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

def stop():
    print("Stopping the motor")
    GPIO.output(16, False)
    GPIO.output(18, False)
    motorSpeed.ChangeDutyCycle(0)

try:
    # Event loop
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            # Right Stick Z-axis for forward/backward control
            if event.code == evdev.ecodes.ABS_RZ:  # Check if the Z-axis is used
                if event.value < 32768:  # Forward movement
                    speed = round(map_value(event.value, 1638, 32768, 100, 0)) # 1638 is 5% of 32768
                    forward(speed)
                elif event.value > 32768:  # Backward movement
                    speed = round(map_value(event.value, 34406, 65535, 0, 100))
                    backward(speed)
                else:  # Neutral position
                    stop()  # Stop the motor if the stick is centered
                print(f"Z-axis value: {event.value} -> Speed: {speed}%")

except KeyboardInterrupt:
    pass
finally:
    stop()  # Ensure the motor is stopped when exiting
    GPIO.cleanup()  # Clean up GPIO settings
