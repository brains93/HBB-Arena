#include <FastLED.h>

// Define which pins to use.
const uint8_t dataPin = A4;
const uint8_t clockPin = A5;

// #define PIN            6  // Pin number to which the data input of the NeoPixel strip is connected
#define NUM_LEDS     30 // Number of LEDs in the strip
#define START_PIN     2  // Pin number to which the button is connected
#define MID_PIN     3  // Pin number to which the button is connected
#define END_PIN     4  // Pin number to which the button is connected


int buttonState = 0;
int startbuttonState = 0;
int midbuttonState = 0;
int endbuttonState = 0;
int lastButtonState = 0;

// Define the array of leds
CRGB leds[NUM_LEDS];


void setup() {
  Serial.begin(9600);
  pinMode(START_PIN, INPUT_PULLUP);
  pinMode(MID_PIN, INPUT_PULLUP);
  pinMode(END_PIN, INPUT_PULLUP);
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, BGR>(leds, NUM_LEDS);
  Serial.println("setup compleate");

  for(int i=0;i<NUM_LEDS;i++){
    leds[i] = CRGB::Red;
  }
}

void loop() {
  // Serial.println("looping");
  
  startbuttonState = digitalRead(START_PIN);
  midbuttonState = digitalRead(MID_PIN);
  endbuttonState = digitalRead(END_PIN);


  if (startbuttonState == LOW) {
     Serial.print("match start pressed");
    // Button was pressed
    start();
  }
  else if (midbuttonState == LOW) {
      Serial.print("match mid pressed"); 

    // Button was pressed
    flashred();
  }
  else if (endbuttonState == LOW) {
    Serial.print("match end pressed");

    // Button was pressed
    endred();
  }
}

void start() {
  flash(3);
  green()
  delay(500)
  white();
  }


void flashred() {
  flash(3);
  white();
  
}

void endred() {
  flash(5);
  red();
 
}

void red(){
   for(int i=0;i<NUM_LEDS;i++){
    leds[i] = CRGB::Red;
  }
  FastLED.show();
}

void green(){
   for(int i=0;i<NUM_LEDS;i++){
    leds[i] = CRGB::Green;
  }
  FastLED.show();
}

void white(){
   for(int i=0;i<NUM_LEDS;i++){
    leds[i] = CRGB::White;
  }
  FastLED.show();
}

void flash(int duration) {
  unsigned long startTime = millis();

  while (millis() - startTime < duration) {
    for(int i=0;i<NUM_LEDS;i++){
      leds[i] = CRGB::Red;
  }
    FastLED.show();
    delay(100); // Adjust the delay to control the flashing speed

    for(int i=0;i<NUM_LEDS;i++){
      leds[i] = CRGB::White;
  }
    FastLED.show();
    delay(100); // Adjust the delay to control the flashing speed
  }
}