"""
Car Module contains the classes 'Device', 'Engine' and'Car'
More Information -> See Class Docs

Authors:    Tom Georgi <Tom.Georgi@htwg-konstanz.de>
            Joshua Rutschmann <Joshua.Rutschmann@htwg-konstanz.de>
"""
from __future__ import print_function

import mraa
import sys
import time
import datetime
from time import sleep
from evdev import InputDevice, ecodes


class Device:
    """
    Class Device creates an Input Device.
    """

    def __init__(self):
        """
        Initialize the device (controller)
        """
        self.__controller = None
        self.__connect_controller()

    def __connect_controller(self):
        """
        Connect controller via Bluetooth and the class 'InputDevice'
        If Controller is not connected with Bluetooth the program exit.
        """
        try:
            self.controller = InputDevice('/dev/input/event2')
        except OSError:
            print('Bluetooth controller not connected.')
            sys.exit(-1)

    @property
    def controller(self):
        """Returns: controller"""
        return self.__controller

    @controller.setter
    def controller(self, value):
        """
        Set controller object.

        Args:
            value: object of InputDevice
        """
        self.__controller = value


class Engine:
    """
    class Engine contains the needed pins.
    """

    def __init__(self):
        """
        Initialize the MRAA library pins
        """
        # Declare MRAA Lib Pins
        self._pin_drive_motor_pwm = mraa.Pwm(0)  # drive_motor_pwm pin
        self._pin_steering_motor_pwm = mraa.Pwm(14)  # steering_motor_pwm
        self._drive_motor_pins = (mraa.Gpio(45), mraa.Gpio(46))  # Direction Forward and Backward
        self._steering_motor_pins = (mraa.Gpio(47), mraa.Gpio(48))  # Direction Left and Right
        self._pin_standby = mraa.Gpio(15)

        self.setup()

    def setup(self):
        """
        Setup the Pin Properties
        """
        self._pin_drive_motor_pwm.enable(True)
        self._pin_steering_motor_pwm.enable(True)

        self._pin_standby.dir(mraa.DIR_OUT)
        self._drive_motor_pins[0].dir(mraa.DIR_OUT)
        self._drive_motor_pins[1].dir(mraa.DIR_OUT)
        self._steering_motor_pins[0].dir(mraa.DIR_OUT)
        self._steering_motor_pins[1].dir(mraa.DIR_OUT)

        self._pin_standby.write(1)
        self._drive_motor_pins[0].write(0)
        self._drive_motor_pins[1].write(0)
        self._steering_motor_pins[0].write(0)
        self._steering_motor_pins[1].write(0)


class Car(Engine):
    """

    """

    _GEAR_SPEED = [(0.0, 0.20), (0.20, 0.35), (0.35, 0.55), (0.55, 0.80), (0.80, 1.00)]

    def __init__(self, dev):
        """

        Args:
            dev:
        """
        Engine.__init__(self)
        self._dev = dev
        self._controller = dev.controller

        self._gear = 0
        self._raw_speed_value = 0
        self._speed_value = 0
        self._old_speed_value = 0
        self._steer_value = 0
        self._old_steer_value = 0
        self._record_mode = False
        self._last_time = None
        self._track = []

    def speed(self, value):
        """

        Args:
            value:

        Returns:

        """
        if value < -0.1:
            self._drive_motor_pins[0].write(0)
            self._drive_motor_pins[1].write(1)
            self._pin_drive_motor_pwm.write(value * -1)
        elif value > 0.1:
            self._drive_motor_pins[0].write(1)
            self._drive_motor_pins[1].write(0)
            self._pin_drive_motor_pwm.write(value)
        else:
            self._drive_motor_pins[0].write(0)
            self._drive_motor_pins[1].write(0)
            self._pin_drive_motor_pwm.write(0)

    def speed_with_gear(self, value, gear):
        """
        """
        min_and_max = Car._GEAR_SPEED[gear]
        speed = None
        if value < 0:
            speed = value
        else:
            if min_and_max[0] <= value:
                if value >= min_and_max[1]:
                    speed = min_and_max[1]
                else:
                    speed = value
            else:
                speed = 0
        
        return speed
            
    def drive_circle(self):
        self.steer(-1)
        sleep(0.3)        
        for i in range(0, 3):
            self.steer(1)
            self.speed(1)
            sleep(3.2)
            
    def steer(self, value):
        """

        Args:
            value:

        Returns:

        """
        if value < -0.1:
            self._steering_motor_pins[0].write(1)
            self._steering_motor_pins[1].write(0)
            self._pin_steering_motor_pwm.write(value * -1)
        elif value > 0.1:
            self._steering_motor_pins[0].write(0)
            self._steering_motor_pins[1].write(1)
            self._pin_steering_motor_pwm.write(value)
        else:
            self._steering_motor_pins[0].write(0)
            self._steering_motor_pins[1].write(0)
            self._pin_steering_motor_pwm.write(0)

    def run(self):
        """
        """
        
        try:
            while True:
                self._read_events()
                
                self._speed_value = self.speed_with_gear(self._raw_speed_value, self._gear)

                self.speed(self._speed_value)
                self.steer(self._steer_value)
                
                if self._record_mode:
                    if self._speed_value != self._old_speed_value or self._steer_value != self._old_steer_value:
                        now = datetime.datetime.now()
                        delta = now - self._last_time
                        self._last_time = now
                        passed_time = delta.seconds + (delta.microseconds / 1000.0 / 1000.0)
                        self._track.append((self._steer_value, self._speed_value, passed_time))
                        self._old_speed_value = self._speed_value
                        self._old_steer_value = self._steer_value

        except KeyboardInterrupt:
            print("Car Stopped.")
        finally:
            self.speed(0)
            self.steer(0)

    def _read_events(self):
        try:
            for event in self._controller.read():
                btn = event.code
                value = event.value

                if btn == ecodes.BTN_TR and value == 1:  # BTN_TR = PS4-Controller R2
                    if self._gear < 4:
                        self._gear += 1
                        print("GEAR: ", str(self._gear))
                elif btn == ecodes.BTN_TL and value == 1:  # BTN_TL = PS4-Controller L2
                    if self._gear > 0:
                        self._gear -= 1
                        print("GEAR: ", str(self._gear))
                elif btn == ecodes.ABS_X:  # ABS_X = PS4-Controller Left Stick
                    if value != 0:
                        self._steer_value = -1.0 * (value / 128.0) + 1.0
                elif btn == ecodes.ABS_RZ:  # ABS_RZ = PS4-Controller Right Stick
                    if value != 0:
                        self._raw_speed_value = - (value / 128.0) + 1.0
                elif btn == ecodes.BTN_B:  # BTN_B = PS4-Controller X
                    self.speed(0)
                    self.steer(0)
                    raise KeyboardInterrupt
                elif btn == ecodes.BTN_Z:
                    if event.value == 1:
                        self.drive_circle()
                elif btn == ecodes.BTN_X:
                    if event.value == 1:
                        self._record_mode = not self._record_mode
                        if self._record_mode:
                            self._track = []
                            self._last_time = datetime.datetime.now()
                        print("Record Mode:", self._record_mode)
                elif btn == ecodes.BTN_A:
                    if event.value == 1 and len(self._track) > 0:
                        print("Replaying record.")
                        for steer, speed, time in self._track:
                            sleep(time)
                            self.steer(steer)
                            self.speed(speed)
                elif btn == ecodes.BTN_C:
                    if event.value == 1 and len(self._track) > 0:
                        print("Replaying record in reverse.")
                        for steer, speed, time in self._track[::-1]:
                            sleep(time)
                            self.steer(steer)
                            self.speed(speed * -1)
        except IOError:
            return  
                

if __name__ == '__main__':
    """ Main """
    controller = Device()
    car = Car(dev=controller)
    car.run()
    exit(0)
