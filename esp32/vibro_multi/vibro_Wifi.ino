#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "Mi Phone";      // Replace with your access point SSID
const char* password = "12341234";  // Replace with your access point password

const int arduinoPort = 25002;      // Port to listen on

int motorPin1 = 13;     // GPIO 13 for vibration motor
int motorPin2 = 12;     // GPIO 13 for vibration motor
int motorPin3 = 27;     // GPIO 13 for vibration motor
int motorPin4 = 33;     // GPIO 13 for vibration motor

char command;           // Variable to store incoming command
int voltage = 0;        // Variable to store the received voltage value

WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  pinMode(motorPin1, OUTPUT);  // Pin configuration
  pinMode(motorPin2, OUTPUT);  // Pin configuration
  pinMode(motorPin3, OUTPUT);  // Pin configuration
  pinMode(motorPin4, OUTPUT);  // Pin configuration

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
  // Check for UDP packets
  int packetSize = udp.parsePacket();
  if (packetSize) {
    // Read incoming data from the UDP packet
    char command = udp.read();
    executeCommand(command);
  }

  // Process other tasks
  // ...
}

void executeCommand(char command) {
  
  switch (command) {
    case '1':  // Command to turn on the motor
      digitalWrite(motorPin1, HIGH);  // Turn on the motor
      break;
    case '2':  // Command to turn off the motor
      digitalWrite(motorPin2, HIGH);  // Turn off the motor
      break;
    case '3':  // Command to turn on the motor
      digitalWrite(motorPin3, HIGH);  // Turn on the motor
      break;
    case '4':  // Command to turn off the motor
      digitalWrite(motorPin4, HIGH);  // Turn off the motor
      break;
    default:
      digitalWrite(motorPin1, LOW);  // Turn on the motor
      digitalWrite(motorPin2, LOW);  // Turn on the motor
      digitalWrite(motorPin3, LOW);  // Turn on the motor
      digitalWrite(motorPin4, LOW);  // Turn on the motor
      break;
  }
}
