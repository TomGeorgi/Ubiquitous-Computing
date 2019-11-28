from time import sleep

import mraa
import sys
from evdev import InputDevice, categorize, ecodes

GEAR = 1

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

# Pinmode set
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


def connect_controller():
    # Declare PS4 Controller
    try:
        return InputDevice('/dev/input/event2')
    except:
        print("Bluetooth Controller not connected.")
        sys.exit(-1)


def print_info(c):
    for event in c.read_loop():
        print(categorize(event))


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


def car(con):
    global GEAR

    for event in con.read_loop():
        if event.code == ecodes.BTN_TR:
            # print("Button TR pressed")
            if event.value == 1:
                # print("Drive Value = 1")
                # pin_standby.write(1)
                if GEAR == -1:
                    GEAR = 1
                elif GEAR < 6:
                    GEAR += 1
                # print("PWM Value: ", str(pin_driveMotorPwm.read()))
            print("Current Gear: ", str(GEAR))
        if event.code == ecodes.BTN_TL:
            # print("Button TL pressed")
            if event.value == 1:
                if GEAR == 1:
                    GEAR = -1
                elif -1 < GEAR <= 6:
                    GEAR -= 1

            print("Current Gear: ", str(GEAR))
        if event.code == ecodes.ABS_X:
            if event.value != 0:
                steer_value = -1 * (event.value / 128.0) + 1.0
                # print("Linker Trigger  - X Achse " + str(event.value) + " | " + str(steer_value))
                steer(steer_value)
        if event.code == ecodes.ABS_RZ:
            if event.value != 0:
                drive_value = - (event.value / 128.0) + 1.0
                # print ("Rechter Trigger - Y Achse " + str(event.value) + " | " + str(drive_value))
                drive(drive_value)
        if event.code == ecodes.BTN_B:
            drive(0)
            steer(0)
            sys.exit(0)
        if event.code == ecodes.BTN_C:
            # Backwards parking
            if event.value == 1:
                steer(-1)
                drive(-0.3)
                sleep(2)
                steer(0)
                sleep(0.5)
                drive(0)

        if event.code == ecodes.BTN_A:
            # Front parking
            pass
        if event.code == ecodes.BTN_X:
            # Side parking
            pass

if __name__ == '__main__':
    controller = connect_controller()
    if sys.argv[1] == "print_info":
        print_info(controller)
    elif sys.argv[1] == "drive":
        car(controller)
