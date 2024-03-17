#include "HardwareSerial.h"
#include <Arduino.h>

// user editable start here

// Number of previous measurement to average out
const int measurementCount = 1; // 500 was good

// Time per measuremes in ms
const int measurementTime = 1;

// Every x measurement to output value to serial
const int displayTimeMultiplyer = 1; // 500 was good

// Voltage divider is connected to GPIO 34 which is an analog pin 
const int potPin = 34;

// user editable ends here

// variable for storing the potentiometer value
int potValue = 0;

short int currentPos = 0;
short int displayMultiplyerCount = 0;

int avePotValue[measurementCount];

void setup() {
    Serial.begin(115200);
    delay(1000);
    potValue = analogRead(potPin);
    for (int i = 0; i < measurementCount; ++i) {
        avePotValue[i] = potValue;
    }
}

void loop() {
    // Reading potentiometer value
    potValue = analogRead(potPin);
    
    avePotValue[currentPos] = potValue;

    int sum = 0;
    for(int i = 0; i<measurementCount; i++){
        sum+=avePotValue[i];
    }
    
    if (displayMultiplyerCount == 0) {
        // if value is maxed out all the way it outputs -1 as it probably means something is not connected
        Serial.println((potValue == 4095) ? -1 : sum/measurementCount);
    }
    
    displayMultiplyerCount = (++displayMultiplyerCount)%displayTimeMultiplyer;
    currentPos = (++currentPos)%measurementCount;
    delay(measurementTime);
}


