// Pin definitions
const int irSensorPin = 2;
const int relayPin = 3;

// Setup function
void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Initialize pins
  pinMode(irSensorPin, INPUT);
  pinMode(relayPin, OUTPUT);

  // Ensure relay is off initially
  digitalWrite(relayPin, LOW);
}

// Loop function
void loop() {
  // Read the state of the infrared sensor
  int irSensorState = digitalRead(irSensorPin);

  // If an object is detected by the infrared sensor
  if (irSensorState == LOW) {
    Serial.println("Object detected!");

    // Activate relay
    digitalWrite(relayPin, LOW);
  } else {
    Serial.println("No object detected.");

    // Deactivate relay
    digitalWrite(relayPin, HIGH);
  }

  // Small delay to avoid rapid state changes
  delay(100);
}
