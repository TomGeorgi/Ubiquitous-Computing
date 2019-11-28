import mraa
import sys
from evdev import InputDevice, categorize, ecodes

#Declare PS4 Controller
try:
    ps4Controller = InputDevice('/dev/input/event2')
except:
    print ("Bluetooth Controller not connected.")
    sys.exit()

#Declare pins
steeringMotorPwm = 14
steeringMotorPin1 = 47
steeringMotorPin2 = 48
driveMotorPwm = 0
driveMotorPin1 = 45
driveMotorPin2 = 46
standby = 15 #TODO

#MRAA Lib pins
pin_driveMotorPwm = mraa.Pwm(driveMotorPwm)
pin_steeringMotorPwm = mraa.Pwm(steeringMotorPwm)

pin_driveMotorPin1 = mraa.Gpio(driveMotorPin1)
pin_driveMotorPin2 = mraa.Gpio(driveMotorPin2)
pin_steeringMotorPin1 = mraa.Gpio(steeringMotorPin1)
pin_steeringMotorPin2 = mraa.Gpio(steeringMotorPin2)

pin_standby = mraa.Gpio(standby)

#Pinmode set
pin_driveMotorPwm.enable(True)
pin_steeringMotorPwm.enable(True)

pin_standby.dir(mraa.DIR_OUT)
pin_driveMotorPin1.dir(mraa.DIR_OUT)
pin_driveMotorPin2.dir(mraa.DIR_OUT)
pin_steeringMotorPin1.dir(mraa.DIR_OUT)
pin_steeringMotorPin2.dir(mraa.DIR_OUT)

pin_standby.write(1)
pin_driveMotorPin1.write(0)
pin_driveMotorPin2.write(0)
pin_steeringMotorPin1.write(0)
pin_steeringMotorPin2.write(0)

def drive(speed):
    if speed < -0.1:
        pin_driveMotorPin1.write(0)
        pin_driveMotorPin2.write(1)
        pin_driveMotorPwm.write(speed * -1)
    elif speed > 0.1:
        pin_driveMotorPin1.write(1)
        pin_driveMotorPin2.write(0)
        pin_driveMotorPwm.write(speed)
    else:
        pin_driveMotorPin1.write(0)
        pin_driveMotorPin2.write(0)
        pin_driveMotorPwm.write(0)

def steer(value):
    if value < -0.1:
        pin_steeringMotorPin1.write(1)
        pin_steeringMotorPin2.write(0)
        pin_steeringMotorPwm.write(value * -1)
    elif value > 0.1:
        pin_steeringMotorPin1.write(0)
        pin_steeringMotorPin2.write(1)
        pin_steeringMotorPwm.write(value)
    else:
        pin_steeringMotorPin1.write(0)
        pin_steeringMotorPin2.write(0)
        pin_steeringMotorPwm.write(0)

def main():
    drive_value = 100
    steer_value = 0
    while True:
        drive(drive_value)

if __name__ == "__main__":
    main()


