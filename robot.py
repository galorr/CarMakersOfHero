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
    pin = 12
    freq = 50
    pi_pwm = None

    def __init__(self,pin,freq,pi_pwm=None):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pi_pwm = GPIO.PWM(self.pin, self.freq)

    def pwm_right(self,start):
        self.pi_pwm.start(start)
        while True:
            print ("Robot turns right")
            # Going right - TBD

    def pwm_left(self,start):
        self.pi_pwm.start(start)
        while True:
            print ("Robot turns right")
            sleep(1)
            # Going left - TBD

    def pwm_straight(self,start):
        self.pi_pwm.start(start)
        while True:
            print ("Robot moving straight")
            sleep(1)
            # Going straight - TBD

    def pwm_differentialFront(self,start):
        self.pi_pwm.start(start)
        while True:
            print ("Robot front differential")
            sleep(1)
            # Going differential - TBD

    def pwm_differentialRear(self,start):
        self.pi_pwm.start(start)
        while True:
            print ("Robot rear differential")
            sleep(1)
            # Going differential - TBD


    def pwm_steering(self, start):
        self.pi_pwm.steering(start)
        while True:
            print("Robot steering")
            sleep(1)
        # Going differential - TBD

    def pwm_right(self,start):
        self.pi_pwm.start(start)
        while True:
            print ("Robot turns right")
            sleep(1)

    def pwm_throttle(self,start):
        self.pi_pwm.start(start)
        while True:
            print ("Robot throttle")
            sleep(1)

    def pwm_lock(self,start):
        self.pi_pwm.start(start)
        while True:
            print ("Robot stops")
            sleep(1)
    # Going right - TBD
    # pi_pwm = GPIO.PWM(pin, freq)
    # #pi_pwm.start(10)
    # pi_pwm.start(10)
    # #GPIO.output(pin, 1400)
    # #GPIO.output(12, GPIO.HIGH)
    # while True:
    #     #for duty in range(0, 101, 1):
    #     #    pi_pwm.ChangeDutyCycle(duty)
    #     #    sleep(0.01)
    #     GPIO.output(pin,1400)
    #     sleep(0.5)
