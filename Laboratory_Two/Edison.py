import mraa
import sys
from evdev import InputDevice, categorize, ecodes

#Declare PS4 Controller
try:
    ps4Controller = InputDevice('/dev/input/event2')
    pass
except:
    print ("Bluetooth Controller not connected.")
    sys.exit()

#Declare pins
driveMotorPwm = 0
driveMotorPin1 = 45
driveMotorPin2 = 46
steeringMotorPwm = 14
steeringMotorPin1 = 47
steeringMotorPin2 = 48
standby = 15

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
    if speed <= -0.1:
        pin_driveMotorPin1.write(0)
        pin_driveMotorPin2.write(1)
        pin_driveMotorPwm.write(speed * -1)
    elif speed >= 0.1:
        pin_driveMotorPin1.write(1)
        pin_driveMotorPin2.write(0)
        pin_driveMotorPwm.write(speed)
    else:
        pin_driveMotorPin1.write(0)
        pin_driveMotorPin2.write(0)
        pin_driveMotorPwm.write(0)

def steer(value):
    if value <= -0.1:
        pin_steeringMotorPin1.write(1)
        pin_steeringMotorPin2.write(0)
        pin_steeringMotorPwm.write(value * -1)
    elif value >= 0.1:
        pin_steeringMotorPin1.write(0)
        pin_steeringMotorPin2.write(1)
        pin_steeringMotorPwm.write(value)
    else:
        pin_steeringMotorPin1.write(0)
        pin_steeringMotorPin2.write(0)
        pin_steeringMotorPwm.write(0)

def main():
    drive_value = 1
    steer_value = 0

    for event in ps4Controller.read_loop():
        if event.type == ecodes.EV_KEY:
            print(categorize(event))
        if event.code == ecodes.BTN_TR:
            print("Button Pressed")
            print(str(event.value))
        # if event.type == ecodes.EV_ABS:
        #     if event.code == ecodes.ABS_X:
        #         steer_value = - (event.value / 128.0) + 1.0
        #         print ("Linker Trigger  - X Achse " + str(event.value) + " | " + str(steer_value))
        #         steer(steer_value)
        #     elif event.code == ecodes.ABS_RZ:
        #         drive_value = - (event.value / 128.0) + 1.0
        #         print ("Rechter Trigger - Y Achse " + str(event.value) + " | " + str(drive_value))
        # elif event.type == ecodes.EV_KEY:
        #     if event.code == ecodes.BTN_TL2:
        #         pin_standby.write(1)
        #         pin_driveMotorPin1.write(0)
        #         pin_driveMotorPin2.write(0)
        #         pin_steeringMotorPin1.write(0)
        #         pin_steeringMotorPin2.write(0)
        #         pin_driveMotorPwm.write(0)
        #         pin_steeringMotorPwm.write(0)
        #         exit()
    try:
        while True:
            drive_value = input()
            drive(drive_value)


    finally:
        drive(0)

if __name__ == "__main__":
    main()

