const int analogInPin1 = 26;
const int analogInPin2 = 25;
const int analogInPin3 = 34;
const int analogInPin4 = 39;
int sensorValue1 = 0;
int sensorValue2 = 0;
int sensorValue3 = 0;
int sensorValue4 = 0;

void setup() {
  // Set the serial monitor baudrate
  Serial.begin(115200);
}

void loop() {

  // Read a 10 bit integer (0 to 1023) from the sensors
  sensorValue1 = analogRead(analogInPin1);
  sensorValue2 = analogRead(analogInPin2);
  sensorValue3 = analogRead(analogInPin3);
  sensorValue4 = analogRead(analogInPin4);

  // Print sensor values
  Serial.print(sensorValue1);
  Serial.print(",");
  Serial.print(sensorValue2);
  Serial.print(",");
  Serial.print(sensorValue3);
  Serial.print(",");
  Serial.println(sensorValue4);
}
