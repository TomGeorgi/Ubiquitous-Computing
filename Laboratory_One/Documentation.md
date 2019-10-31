# Laboratory 1: Arduino

## 1 Basic working with Arduino IO, PWM and Serial

```
Give a short overview about the IO of Arduino, what pins are and what kind of pins are there and how to use them.
```
- A0 to A5 are **analog** inputs with a resolution of 
- 1 to 13 are **digital** In- and Outputs (0 -> **RX**, 1 -> **TX**, 3/5/6/9/10/11 -> **PWM capable**)
- AREF is a pin to supply the reference voltage for the analog inputs.
- SDA & SCL are part of the I²C interface

## 1.1 First Task to be done

```
Make an LED Blink and Fade. What is the difference between the two ways to realize it ? Describe it in few words and give an example. You can use the tutorial.
```

If you want the LED to fade you need a PWM Signal which can be send via the command `analogWrite(...)`. If you want that the LED should blink you need a digital Signal which can be send via the command `digitalWrite(...)`.

## 1.2 Second Task to be done

```
Make a Buzzer Program. Describe it in few words and give an example how it works. What is needed to make it Buzz ?
```

With the function `tone(pin, frequency, duration)` which we will pass the pin to which the buzzer is connected. We also pass a frequency and the duration of the note in milliseconds


## 1.3 Third Task to be done

```
Expand the Blink Task with a button or a timer and a Buzzer. Create a Program that uses the knowledge of the last exercises. Describe in few words how it works.
```

The button will be connected to an IO Pin (e.g Pin 7). If the Button is pressed the IO Pin returns a HIGH (=1) Flank. So if this Pin returns 1 the LED turn on. When the button is released the IO Pin returns a LOW (=0) Flank and we can turn off the LED. 

## 1.4 Fourth Task to be done

```
Communication between different modules: Understand the Serial communication. 
Read and understand what Serial communication is. What other kind of communication possibilities options are there and what are their advantages and disadvantages. Describe at least two additional communication methods and Serial.
```

There are also I²C and SPI. Comparing to Serial I²C is synchronous (it has a clock pin). The disadvantage of I²C is its limited speed. SPI on the other hand needs more cables but you can also chain multiple SPI capable devices in series.


## 1.5 Fifth Task to be done

```
Combine Task 1.1 to 1.4. Be creative
Create a Program that uses LED, Buzzer, timer and serial communication. Describe what your idea is and how you realized them.
```

The button will be used to create a circuit. If the button is pressed the circuit will be closed and the connected Pin will get a HIGH flank. We can read the value of the Pin in our Program which Value it has. As an example: If the button was pressed the Flank from the connected IO Pin will be HIGH (=1). So if the this Pin is 1 we can turn on a LED or something else. If the Pin returns 0 we can turn off the LED.

## 2 LED Matrix

## 2.1 First Task to be done

```
Given the Hardware (Arduino + LED Matrix 16x8 LED) do a counter and a small application. Read the documentation of the module and apply. Explain how it works and what is necessary. Also describe the parameters.
```

## 2.2 Second Task to be done

```
Count with the LED from 0 to 128. As Tipp: use the function "matrix.drawPixel(X, Y, COLOR);". How does the function work ? What are parameters. How do you make the content fit ?
```

The parameters *X* and *Y* are the coordinates of the pixel which should be set. Because we only have one color we pass LED_ON as the third parameter.


## 2.3 Third Task to be done

```
Draw easy Bitmap on the LED Matrix. As Tipp: use the function "matrix.drawBitmap(0, 8, om_bmp, 8, 8, HT16K33_BLINK_CMD);". How does this function work ? What else is necessary ?
```

It takes a bitmap *matrix* (progmem uint8 array) and "puts" it onto the matrix.

## 2.4 Fourth Task to be done

```
Print some Text in the LED Matrix. As Tipp: use the functions "matrix.print("Hello");" and "matrix.setCursor(x, 0);". How does this work ? What options are available ? How does the example behave with more longer text ? What happens with the memory ? 
```

## 2.5 Fifth Task to be done

```
Document and explain all functions and how does the Board work.
```

## 3 LED Matrix as Terminal Output

```
Combine the knowledge of the two previous Tasks and write a LED-Banner that plots the data that is send the Arduino via Terminal. Describe how your program works and what your concept is. Do some sort of planning before you start programming.
```

We use `Serial.read()` to read from the Arduino terminal. The returned string is then printed onto the matrix.


## 4 Wire layout for temperature measurement (Arduino)

```
Wire layout for temperature measurement
In the first part of the laboratory we will connect the digital thermometer (DS18B20) and the Arduino Uno, in order to get data from the digital sensor and to measure the temperature.
You need the following:
    - 1 or more digital thermometer (DS18B20)
    - 1 Arduino Uno or similar board.
    - 1 resistor (4,7K Ω)
    - Cables (Vcc = red, GND = black)
    - 1 Breadboard (grey element in the figure)
```

## 4.1 Implementation

```
The digital thermometer uses a one-wire protocol for communication. Fortunately the Arduino IDE already provides an implementation for the protocol (one-wire library). For this exercise we will use the already existing library. 
```

## 4.2 Temperature reading

```
Using the Arduino implement a algorithm to get the data from the sensor and plot it onto the serial console
```

## 4.3 LED scale

```
Extend the circuit with a LED Matrix and display the temperature
```