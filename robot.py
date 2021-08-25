from zmq.sugar.constants import NULL
import RPi.GPIO as GPIO
from time import sleep
#
# Robot moves
#
#
# "differentialFront"
# "differentialRear"
# "steering"
#  throttle"
#
class Robot:
    # Pin Definitions:
    pinSteering = 7 # steer right
    pinThrottle = 15 # throttle forword/backword
    pinDifferentialFront = 8 # differential front
    pinDifferentialBack = 16 # differential back

    dc = 95 # duty cycle (0-100) for PWM pin
    freq = 50

    # PWM Definitions:
    pwmLock = None
    pwmSteering = None
    pwmThrottle = None
    

    def __init__(self):
        GPIO.setwarnings(False)
        # Pin Setup:
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(self.pinDifferentialFront, GPIO.OUT) # DifferentialFront pin set as output
        GPIO.setup(self.pinDifferentialBack, GPIO.OUT) # DifferentialBack pin set as output
        GPIO.setup(self.pinSteering, GPIO.OUT) # Steering pin set as output
        GPIO.setup(self.pinThrottle, GPIO.OUT) # Throttle pin set as output

        # PWM Definitions:
        self.pwmDifferentialFront = GPIO.PWM(self.pinDifferentialFront, self.freq)
        self.pwmDifferentialBack = GPIO.PWM(self.pinDifferentialBack, self.freq)
        self.pwmSteering = GPIO.PWM(self.pinSteering, self.freq)
        self.pwmThrottle = GPIO.PWM(self.pinThrottle, self.freq)

        # PWM Start
        self.pwmDifferentialFront.start(1000)
        self.pwmDifferentialBack.start(1000)
        self.pwmSteering.start(1500)
        self.pwmThrottle.start(1500)

    def pwm_steering(self, start):
        while True:
            print("Robot steering")
            self.pwmSteerLeft.ChangeDutyCycle(self.dc)
            GPIO.output(self.pinSteerLeft, start)
            sleep(1)

    def pwm_throttle(self,start):
        while True:
            print ("Robot throttle")
            self.pwmThrottle.ChangeDutyCycle(self.dc)
            GPIO.output(self.pinThrottle, start)
            sleep(1)

    def pwm_lock(self,start):      
        while True:
            print ("Robot lock")
            self.pwmDifferentialFront.ChangeDutyCycle(self.dc)
            self.pwmDifferentialBack.ChangeDutyCycle(self.dc)
            GPIO.output(self.pinDifferentialFront, start)
            GPIO.output(self.pinDifferentialBack, start)
            sleep(1)

    def stop(self):
        self.pwmDifferentialFront.stop() # stop pwmDifferentialFront
        self.pwmDifferentialBack.stop() # stop pwmDifferentialBack
        self.pwmThrottle.stop() # stop pwmThrottle
        self.pwmSteering.stop() # stop pwmSteering
        GPIO.cleanup() # cleanup all GPIO
