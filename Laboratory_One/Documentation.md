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

1. Task Definition

    Make an LED Blink and Fade. What is the different between the two ways to realize it? Describe it
    in few words and give an example. You can use the tutorial as base. Don’t forget to explain the
    difference concepts and ideas behind Blink and Fade. Give also a short use case for each of this
    concepts.

2. Evaluation
   
    If you want the LED to fade you need a PWM Signal which can be send via the function `analogWrite(pin, value)`. If you want that the LED should blink you need a digital Signal which can be send via the function `digitalWrite(pin, value)`.

    The example below shows how the function `digitalWrite()` does work for a LED which should be glow for one second:

    ```arduino

    int led = 7;

    void setup() {
        pinMode(led, OUTPUT);    // Set Mode for our Pin to "Output".
        digitalWrite(led, HIGH); // Set the flank on our Pin to High (LED is on).
        delay(1000);             // Wait for 1000ms (= 1s).
        digitalWrite(led, LOW);  // Set the flank on our Pin to Low (LED is off).
    }

    ```

    We can see that the function is kept very simple.
    The example below shows how we can set different values for an digital PWM Pin.

    ```arduino

    int led = 9; // Digital PWM Pin

    void setup() {
        int value = 42;
        analogWrite(led, value); // Set Value on our Pin to 42.
        value = 255;
        analogWrite(led, value); // Set Value on our Pin to 255;
        value = 0;
        analogWrite(led, value); // Set Value on our Pin to 0;
    }

    ```

    Now we can see the function `analogWrite()` can set more different values (from 0 to 255) as the function `digitalWrite()`.

## 1.2 Second Task to be done

1. Task Definition

    Make a Buzzer Program. Describe it in few words and give an example how it works. What is
    needed to make it Buzz. Implement your own melody and describe how to create a melody or how
    to implement a song. Give also a short use case for each of this concepts.

2. Evaluation

    With the function `tone(pin, frequency, duration)` which we will pass the pin to which the buzzer is connected. We also pass a frequency and the duration of the note in milliseconds.

    For example:
    ```arduino

    void setup() {
        tone(8, random(100,2000), random(100, 2000));
    }

    ```

    The example above sets a frequenz between 100 and 2000 Hz on Pin 8 with a Duration between 100ms and 2000ms.

## 1.3 Third Task to be done

1. Task Definition:
    
    Expand the Blink Task with a button or a timer and a Buzzer. Create a Program that uses the knowledge of the last exercises. Describe it in few words how the program works. Describe the idea behind the program.

2. Evaluation:

    The button will be connected to an IO Pin (e.g Pin 7). If the Button is pressed the IO Pin returns a HIGH (=1) Flank. So if this Pin returns 1 the LED turn on. When the button is released the IO Pin returns a LOW (=0) Flank and we can turn off the LED. 

## 1.4 Fourth Task to be done

1. Task Definition: 
   
    Read and understand what Serial communication is. What other kind of communication exist for Arduino? What are their advantages and disadvantages? Describe at least two additional communication possibilities additionally to Serial communication.

2. Evaluation:
    
    There are also I²C and SPI. Comparing to Serial I²C is synchronous (it has a clock pin) and so you do not have to agree on a baudrate. The disadvantage of I²C is its limited speed which ranges from 0,1 Mbit/s to 3,4 Mbit/s. The ultra fast mode reaches 5,0 Mbit/s but then it is only unidirectional. Another disadvantage is that I²C is like Serial only half-duplex.
    SPI on the other hand needs more cables but is full-duplex and you can also chain multiple SPI capable devices together.
     You need:
    - SCLK (Serial Clock) Master this emits for synchronisation
    - MOSI (Master Output, Slave Input)
    - MISO (Master Input, Slave Output)


## 1.5 Fifth Task to be done

1. Task Definition:

    Combine task 1.1 to 1.4. Be creative. Describe, imagine a useful application with Arduino. Be creative. Create a program that uses LED, Buzzer, timer and serial communication. Describe what is your idea and how do you realize it.

2. Evaluation:
   


## 2 LED Matrix

## 2.1 First Task to be done

1. Task Definition:
    
    Given the Hardware (Arduino + LED Matrix 16X8 LED or Display) implement a counter and a small application. Read the documentation of the module and apply. Explain how the matrix or display works and what is necessary to get started. Also describe witch parameters are important.

2. Evaluation:

    The given LED Matrix can be controlled with the function `matrix.drawPixel`

## 2.2 Second Task to be done

1. Task Definition:
   
    Count with the LED from 0 to 128. Does the number fit in the Matrix? What can you do to make the numbers fit If you are using the display does how to make the numbers beiger and readable?  As Tipp use the function `matrix.drawPixel(X, Y, COLOR)`. How does this function work? What are the parameters. How do you make the content fit better?

2. Evaluation:

    With the parameters *X* and *Y* we can set the coordinates of the pixel on the given board. With the *COLOR* parameter we can set a value to pixel. In our case we want to activate the LED so we pass the constant `LED_ON` as the third parameter to the function. To see something we need to call the function `matrix.writeDisplay()`.


## 2.3 Third Task to be done

1. Task Definition:
    
    Draw easy Bitmap on the LED Matrix or Display. How does this function work? What else is necessary? How is the Bitmap be stored?
    As Tipp use the function “matrix.drawBitmap(0, 8, om_bmp, 8, 8, HT16K33_BLINK_CMD);”

2. Evaluation: 

    The function `matrix.drawBitmap(x, y, bitmap[], width, height, color)` can render an array onto the board. We can say on which position we want to start, which height and width our Bitmap have and which color we want. In Addition to see something we can put an array as a parameter to this function which will be rendered to our board. To see something on the board we need to call the function `matrix.writeDisplay()` after that.

## 2.4 Fourth Task to be done

1. Task Definition:

    Print some Text in the LED Matrix. How does this work? What options are available? How does the example behave with longer text? How does it work? What happens whit the memory? 
    As Tipp use “matrix.print("Hello");” and “matrix.setCursor(x,0);”

2. Evaluation: 

    With the function `matrix.setCursor(x, 0)` we can set the pixel position where to render the text. For example `matrix.setCursor(0, 0)` sets the pixel position on top left and `matrix.setCursor(15, 0)` set it on top right on our board. With the function `matrix.print("Hello")` we can render the given String (e.g. "Hello") to our board.

## 2.5 Fifth Task to be done

1. Task Definition:

    Give a short overview and explain the most important functions and how does the Board work.

2. Evaluation:



## 3 LED Matrix as Terminal Output

1. Task Definition:
   
    Combine the knowledge of the two previous Tasks and write a LED-Banner that plots the data that is send the Arduino via Terminal. The data should be typed in a serial console and be displayed on the arduino.
    Describe how your program works and what is your concept. Do some sort of planning before you start programing.

2. Concept:

    First of all we have considered how we can get the data from the serial Interface and what happens if there is no data to read. The next thing was how we can print the read data onto the LED Matrix board. So we knew that we need to prepare the board every time we get new data from the serial interface. To read the data from the serial interface we will use the `Serial`-library. 

3. Evaluation: 

    To hack the serial Interface we used the Functions from the `Serial` library. First of all we checked if something is available on the Interface with the function `Serial.available()`. If the return value is greater than 0 then we start reading the data with the function `Serial.readString()` which will be return the data in form of a String.
    After we read the String from the serial interface we prepare our LED matrix board for it. We set the text size to the minimal text size with the function `matrix.setTextSize(1)`, setup the text color with `matrix.setTextColor(LED_ON)`. In Addition we set the start pixel at 0, 0 with the function `matrix.setCursor(0, 0)` and rotate the text 90° with the function `matrix.setRotation(1)`, so that the text will show vertically on the board. The last thing we need to do is to clear the board with `matrix.clear()`. After the preparation we can write the read String with the function `matrix.print()`.


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

1. Task Definition: 

    The digital thermometer uses a one-wire protocol for communication. Fortunately the Arduino IDE already provides an implementation for the protocol (one-wire library). For this exercise we will use the already existing library. Just download it (http://playground.arduino.cc/Learning/OneWire) and integrated it into the Arduino IDE.

2. Evaluation:
   
    First of all we include the downloaded `OneWire`-library. After them we can create an OneWire object for our *DS18B20 Temperature chip* with `OneWire ds(pin)`. In our loop function we setup a `byte addr[8]` and a `byte data[12]` variable. The next thing we need to do is to search the address of our Temperature chip which will be used to start the conversation with the chip. To get the adress we use the function `ds.search(addr)`. This function returns wheter True or False. If an adress was found it will be written into our variable `addr`. After them we reset our Pin, select our found address and start the conversation with `ds.write(0x44, 1)`. After them we can read the values with `ds.read()` into our variable `data`.

## 4.2 Temperature reading

1. Task Definition: 
   
    Using the Arduino implement get the data from sensor and plotted at the Serial console.

2. Evaluation:

    In Addition to 4.1 ...

## 4.3 LED scale

1. Task Definition: 
    
    Expand the circuit with LED Matix and Print the Temperature.

2. Evaluation:

    In Addition to 4.1 and 4.2 ...