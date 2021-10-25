from zmq.sugar.constants import NULL
import RPi.GPIO as GPIO
from time import sleep
#
# Robot moves
#
#
# "steering"
#  throttle"
#
class Robot:
    # Pin Definitions:
    pinSteering = 7 # steer right
    pinThrottle = 15 # throttle forword/backword

    dc = 100 # duty cycle (0-100) for PWM pin
    freq = 50

    # PWM Definitions:
    pwmLock = None
    pwmSteering = None
    pwmThrottle = None
    
    def __init__(self):
        GPIO.setwarnings(False)
        # Pin Setup:
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(self.pinSteering, GPIO.OUT) # Steering pin set as output
        GPIO.setup(self.pinThrottle, GPIO.OUT) # Throttle pin set as output

        # PWM Definitions:
        self.pwmSteering = GPIO.PWM(self.pinSteering, self.freq)
        self.pwmThrottle = GPIO.PWM(self.pinThrottle, self.freq)

        # PWM Start
        self.pwmSteering.start(1500)
        self.pwmThrottle.start(1500)

    def pwm_steering(self, value):
        while True:
            print("Robot steering {}".format(value))
            self.pwmSteering.ChangeDutyCycle(self.dc)
            self.pwmSteering.ChangeFrequency(value)
            GPIO.output(self.pinSteering, value)
            sleep(1)

    def pwm_throttle(self,value):
        while True:
            print("Robot throttle {}".format(value))
            self.pwmThrottle.ChangeDutyCycle(self.dc)
            self.pwmThrottle.ChangeFrequency(value)
            GPIO.output(self.pinThrottle, value)
            sleep(1)

    def stop(self):
        self.pwmThrottle.stop() # stop pwmThrottle
        self.pwmSteering.stop() # stop pwmSteering
        GPIO.cleanup() # cleanup all GPIO
