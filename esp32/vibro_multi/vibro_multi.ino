const int motorPin1 = 13;
const int motorPin2 = 12;
const int motorPin3 = 27;
const int motorPin4 = 33;
String dataStr;
int values[4];
int idx = 0;


void setup() {
  // Set the serial monitor baudrate
  Serial.begin(115200);
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);

  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
   
}

void loop() {
  // Disable all motors

  // Check if there is a serial connection
  if (Serial.available() > 0) {
    // Read in the string from the serial port
    dataStr = Serial.readStringUntil('\n');

    // Iterate until the end of the string
    while (dataStr.length() > 0) {
      int separatorIdx = dataStr.indexOf(',');
      // Breat out of the loop if you reach the end of the string
      if (separatorIdx == -1) {
        values[idx++] = dataStr.toInt();
        break;
      }
      // Continue iterating over the string
      else {
        values[idx++] = dataStr.substring(0, separatorIdx).toInt();
        dataStr = dataStr.substring(separatorIdx+ 1);
      }
    }
    idx = 0;

    Serial.print(values[0]);
    Serial.print(",");
    if (values[0] > 0) {
      digitalWrite(motorPin1, HIGH);
      delay(500);
      digitalWrite(motorPin1, LOW);
      // Serial.print("1");
      // Serial.print(",");
    }

    Serial.print(values[1]);
    Serial.print(",");
    if (values[1] > 0) {
      digitalWrite(motorPin2, HIGH);
      delay(500);
      digitalWrite(motorPin2, LOW);
      // Serial.print(",");
    }

    Serial.print(values[2]);
    Serial.print(",");
    if (values[2] > 0) {
      digitalWrite(motorPin3, HIGH);
      delay(500);
      digitalWrite(motorPin3, LOW);
      // Serial.print("1");
      // Serial.print(",");
    }

    Serial.print(values[3]);
    Serial.print(",");
    if (values[3] > 0) {
      digitalWrite(motorPin4, HIGH);
      delay(500);
      digitalWrite(motorPin4, LOW);
      // Serial.println("1");
    }

  }
}
