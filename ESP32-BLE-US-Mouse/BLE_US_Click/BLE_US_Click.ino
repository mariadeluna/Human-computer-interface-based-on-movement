
#include <BleMouse.h>
//
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLE2902.h>
#include <BLEHIDDevice.h>
#include <HIDTypes.h>

BleMouse bleMouse;

// Ultrasonic pins setup:
const int Trigger = 2;
const int Echo = 3;
const int LED_PIN = 13; // HIGH when detects a threshold

const int threshold = 10; // Threshold distance (cm)
long duration, distance;

//
// BLE configuration
BLEHIDDevice* hid;
BLECharacteristic *inputMouse;
bool deviceConnected = false;




// Calculate the distance using the ultrasonic sensor
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

// Callbacks BLE server
class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
  }

  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
  }
};

void setup() {

  // Ultrasonic sensor and LED configuration 
  pinMode(Trigger, OUTPUT);
  pinMode(Echo, INPUT);
  pinMode(LED_PIN, OUTPUT); // LED is configurated as an output
  digitalWrite(LED_PIN, LOW); // LED initially turn off

  Serial.begin(115200);
  
  // Initialize BLE
 BLEDevice::init("BLE_Ultrasonic_Mouse");  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  bleMouse.begin();
}

void loop() {

  // Measures distance
  long distance = readUltrasonicDistance();
  Serial.print("Distancia: ");
  Serial.println(distance);


  if(bleMouse.isConnected() && distance < threshold) {
    Serial.println("Left click");
    bleMouse.click(MOUSE_LEFT);
    digitalWrite(LED_PIN, HIGH); // LED turns on

    delay(500);
  } else{
    digitalWrite(LED_PIN, LOW); // LED turns off
  }
  delay(100);
}
