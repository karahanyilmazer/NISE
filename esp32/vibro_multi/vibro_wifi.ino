#include <WiFi.h>
#include <WiFiUdp.h>

#include <LinkedList.h>
LinkedList<String> commandList;

const char* ssid = "Mi Phone";//"PYUR 122A2";      // Replace with your access point SSID
const char* password = "12341234";//"nx5rpttK2dXk";  // Replace with your access point password

const int arduinoPort = 25002;      // Port to listen on

int motorPin1 = 13;     // GPIO 13 for vibration motor
int motorPin2 = 12;     // GPIO 13 for vibration motor
int motorPin3 = 27;     // GPIO 13 for vibration motor
int motorPin4 = 33;     // GPIO 13 for vibration motor

int button = 36;     // GPIO 13 for vibration motor

char command;           // Variable to store incoming command
int voltage = 0;        // Variable to store the received voltage value
//int CueValue1 = LOW;
//int lastB = LOW;
int buttonState = HIGH;   // Current state of the button
int lastButtonState = HIGH;  // Previous state of the button
unsigned long lastDebounceTime = 0;  // Last time the button state changed
unsigned long debounceDelay = 50;    // Debounce time in milliseconds

WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  pinMode(motorPin1, OUTPUT);  // Pin configuration
  pinMode(motorPin2, OUTPUT);  // Pin configuration
  pinMode(motorPin3, OUTPUT);  // Pin configuration
  pinMode(motorPin4, OUTPUT);  // Pin configuration
  pinMode(button, INPUT);   // Pin configuration  INPUT_PULLUP

//  attachInterrupt(digitalPinToInterrupt(button), buttonPressed, FALLING);

  // Connect to your local Wi-Fi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  // Print the ESP32's IP address
  Serial.println(WiFi.localIP());

  // No need to set up a server for UDP
  // Set up UDP
  udp.begin(arduinoPort);
  Serial.println("UDP server started");
}

void loop() {
  
  int packetSize = udp.parsePacket();
  char buffer[3];
  if (packetSize) {
    // Read incoming data from the UDP packet
    udp.read(buffer, sizeof(buffer));
    String command = String(buffer);

    if (commandList.get(0)==""){    //if (commandList.isEmpty()) {
      executeCommand(command);  
    }
    commandList.add(command);
  }
  
  int reading = digitalRead(button);

  // Perform debounce
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  // Check if the button state has been stable for the debounce delay
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // Check if the button state has changed
    if (reading != buttonState) {
      buttonState = reading;

      // Check if the button is pressed (LOW)
      if (buttonState == LOW) {
        // Print the value when the button is pressed
        Serial.println("Button pressed!");
//        Serial.println(commandList);
        if (commandList.get(0)!=""){   //(!commandList.isEmpty()) {
          Serial.println("First Letter");
          String firstCommand = commandList.get(0);
          executeCommand(firstCommand); //executeCommand(commandList.get(0));
          commandList.remove(0);
        }
      }
    }
  }
  lastButtonState = reading;
}

void executeCommand(String command) {
  for (int i = 0; i <= 2; i++) {
    char element = command[i];
    switch (element) {
    case '1':  // Command to turn on the motor
      digitalWrite(motorPin1, HIGH);  // Turn on the motor
      delay(500);
      digitalWrite(motorPin1, LOW);  // Turn on the motor
      break;
    case '2':  // Command to turn off the motor
      digitalWrite(motorPin2, HIGH);  // Turn off the motor
      delay(500);
      digitalWrite(motorPin2, LOW);  // Turn on the motor
      break;
    case '3':  // Command to turn on the motor
      digitalWrite(motorPin3, HIGH);  // Turn on the motor
      delay(500);
      digitalWrite(motorPin3, LOW);  // Turn on the motor
      break;
    case '4':  // Command to turn off the motor
      digitalWrite(motorPin4, HIGH);  // Turn off the motor
      delay(500);
      digitalWrite(motorPin4, LOW);  // Turn on the motor
      break;
    default:
      digitalWrite(motorPin1, LOW);  // Turn on the motor
      digitalWrite(motorPin2, LOW);  // Turn on the motor
      digitalWrite(motorPin3, LOW);  // Turn on the motor
      digitalWrite(motorPin4, LOW);  // Turn on the motor
      break;
  }
  delay(250);
  }
//  command = "";
}
//
//void buttonPressed() {
//  // This function will be called when the button is pressed (LOW)
//  Serial.println("Button pressed!");
//  Serial.println(analogRead(button));
//
//  // You can add any other code you want to execute when the button is pressed
//}
