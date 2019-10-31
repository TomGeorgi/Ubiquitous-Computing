#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

#ifndef _BV
  #define _BV(bit) (1<<(bit))
#endif


Adafruit_8x16matrix matrix = Adafruit_8x16matrix();

uint8_t counter = 0;

static const uint8_t PROGMEM frown_bmp_p[] =
{ B01000010,
  B10100101,
  B01100110,
  B00100100,
  B00100100,
  B00111100,
  B00100100,
  B00011000,
  // Second
  B00011000,
  B00100100,
  B00111100,
  B00100100,
  B00100100,
  B01100110,
  B10100101,
  B01000010};

static const uint8_t PROGMEM frown_bmp[] =
{ B00000000,
  B00000000,
  B01110000,
  B00011000,
  B01111101,
  B10110110,
  B10111100,
  B00111100,
  B00111100,
  B10111100,
  B10110110,
  B01111101,
  B00011000,
  B01110000,
  B00000000,
  B00000000};

void setup() {
  Serial.begin(9600);
  Serial.println("HT16K33 test");
  
  matrix.begin(0x70);  // pass in the address
}

void loop() {
  // paint one LED per row. The HT16K33 internal memory looks like
  // a 8x16 bit matrix (8 rows, 16 columns)
  for (uint8_t i=0; i<8; i++) {
    for (uint8_t j=0; j<16; j++) {
      // draw a diagonal row of pixels
      matrix.clear();
      matrix.drawPixel(i, j, LED_ON);
      matrix.drawPixel((8 - i), (16 - j), LED_ON);
      matrix.writeDisplay();
      delay(10);
    }
  }
  for (uint8_t i=0; i<16; i++) {
    for (uint8_t j=0; j<8; j++) {
      // draw a diagonal row of pixels
      matrix.clear();
      matrix.drawPixel(j, i, LED_ON);
      matrix.drawPixel((7 - j), (15 - i), LED_ON);
      matrix.writeDisplay();
      delay(20);
    }
  }
  matrix.clear();
  matrix.writeDisplay();
  delay(100);

  for (uint8_t i=0; i<10; i++) {
    matrix.drawBitmap(0,0, frown_bmp, 8,16, HT16K33_BLINK_CMD);
    matrix.writeDisplay();
    delay(50);
    matrix.clear();
    matrix.writeDisplay();
    delay(50);
  }

  matrix.setRotation(1);
  matrix.setCursor(0, 0);
  matrix.print("Hi");
  matrix.writeDisplay();
  delay(1000);
  matrix.setRotation(0);
  matrix.clear();
  
  
}
