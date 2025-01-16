
#include <BleMouse.h>

// bluetooth connection
BleMouse bleMouse;

// Ultrasonic pins setup:
const int Trigger = 2;
const int Echo = 3;
const int LED_PIN = 13; // HIGH when detects a threshold

const int threshold = 10; // Threshold distance (cm)
long duration, distance;


// calculate the distance using the ultrasonic sensor
long readUltrasonicDistance() {
  digitalWrite(Trigger, LOW);
  delayMicroseconds(2);
  digitalWrite(Trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(Trigger, LOW);
  duration = pulseIn(Echo, HIGH);
  distance = duration / 58;  // Time --> distance (cm)
  return distance;
}

void setup() {

  // ultrasonic sensor and LED configuration 
  pinMode(Trigger, OUTPUT);
  pinMode(Echo, INPUT);
  pinMode(LED_PIN, OUTPUT); // LED is configurated as an output
  digitalWrite(LED_PIN, LOW); // LED initially turned off

  Serial.begin(115200);
  Serial.println("Starting BLE work!");
  bleMouse.begin();
}

void loop() {

  // Measures distance
  long distance = readUltrasonicDistance();
  Serial.print("Distance measured: ");
  Serial.println(distance);

  // if the sensor detects a distance lower than the threshold
  if(bleMouse.isConnected() && distance < threshold) {
    Serial.println("Left click ");
    bleMouse.click(MOUSE_LEFT);
    digitalWrite(LED_PIN, HIGH); // LED turns on

    delay(500);
  } else{
    digitalWrite(LED_PIN, LOW); // LED turns off
  }
  delay(100);
}
