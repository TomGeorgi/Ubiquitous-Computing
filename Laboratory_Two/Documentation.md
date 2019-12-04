# Laboratory 2: Edison autonomous car
#### by Tom Georgi & Joshua Rutschmann

## 0. Exercise

    Design a remote controlled system that drives the car. The main functionality is driving back and forwards, left and right. As remote operator you can use a PS4 Controller, a Web Interface or an App on a smartphone.

## 1. Design Concept

-
    The construction of our remote-controlled car consists of three connected components: Car hardware, control software and remote control. Using the control software written by us, the commands sent by the remote controller are captured and processed in form of events.
    After the events have been processed by the control software, the results should be sent to the hardware installed in the car.
    This should make it possible to control the car remotely.

## 2. Conntect to a PS4 Remote Controller

-
    The task was to select a remote control with which it should be possible to control the car remotely. The following were available:
    - PS4-Controller
    - WebInterface
    - Keyboard
    - Smartphone App
  
- 
    We chose the PS4 controller because:
    - it reminds more of a remote controlled auto than a keyboard or a web interface.
    - it would also be so easy to use for e.g. children
    - the connection between car and PS4 controller is very simple and fast to make.

## 2.1. Advantages

-
    The advantage of the PS4 controller is its ease of use. 
    If you compare this e.g. with a keyboard, a PS4 controller has a manageable number of possibilities to control the car, while a keyboard has much more control possibilities. This can be an advantage if you have a lot of control commands, but in our case it is a disadvantage because it makes our program much more complex for the end user. 
    
    As an example: If the user wants to drive forward, he simply presses the stick forward on the controller, while he could also enter the speed value via a number on the keyboard. This would give the user much more control options, but it would also make the program more error-prone. This is normally not the case with the PS4 controller. Here it is calculated depending on the position of the stick and the car is passed on. 
    
    Another advantage is the connection of controller and car. Once the devices are paired with each other, a Bluetooth connection is automatically established the next time both devices are started.

    In addition, there is the type of connection. While e.g. a keyboard or a web interface requires an intact network connection on the control device (host computer) as well as on the car (target computer) itself, the PS4 controller only requires an activated Bluetooth connection. The advantage is that the Bluetooth connection is less prone to errors and you can use the car regardless of the location.

## 2.2 Disadvantages

-
    A disadvantage of the PS4 controller is the visualization. While you can transmit information to the user via the graphical interface of a web interface, a keyboard program or a smartphone app, this is completely omitted with the PS4 controller. For example, you don't notice if the car or the code has an error that could lead to an abort. With the other control types, errors are faster and easier to recognize, because you can log them and then output them to a graphical interface. 

    Another disadvantage is the termination condition. While with the other remote controllers the catching of exceptions is mostly supported by the programming language and can be handled much easier. This is also possible with the PS4 controller, but much more difficult to realize.

    As an example: If 'Ctrl-C' is pressed on the keyboard, an error called 'KeyboardInterrupt' is thrown in the programming language Python. This error can be caught and treated as a program abort. If you press a defined key on the PS4 controller, which should lead to the termination of the program, all previously received events are processed first. This can lead to accidents during long running tasks, which could damage the car. You could run the long-running tasks in a thread, but it would increase the complexity of the program. That's why we see this as a disadvantage.


## 3. Program Design
## 4. Autonomous car features