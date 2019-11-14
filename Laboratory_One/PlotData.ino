#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

Adafruit_8x16matrix matrix = Adafruit_8x16matrix();

String incomingString = ""; // for incoming serial data
int len = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("16x8 LED Matrix Test");

  matrix.begin(0x70);  // pass in the address
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingString = Serial.readString();
    len = incomingString.length();

    matrix.setTextSize(1);
    matrix.setTextWrap(false);  // we dont want text to wrap so it
scrolls nicely
    matrix.setTextColor(LED_ON);
    matrix.setRotation(1);
    matrix.setCursor(0, 0);
    matrix.clear();

    // say what you got:
    Serial.print("I received: ");
    Serial.println(incomingString);
  }
  else {
    for (int8_t x=7; x>=-(len * 6); x--) {
      matrix.clear();
      matrix.setCursor(x,0);
      matrix.print(incomingString);
      matrix.writeDisplay();
      delay(100);
    }
  }
}