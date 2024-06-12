int RPWM = 10;
int LPWM = 11;
int L_EN = 13;
int R_EN = 12;
int potPin = A1;
int infraredPin = 7; // Pin sensor infrared
int relayPin = 8; // Pin relay
int potValue;
int motorSpeed;

void setup() {
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);
  pinMode(potPin, INPUT);
  pinMode(infraredPin, INPUT);
  pinMode(relayPin, OUTPUT);
  
  digitalWrite(R_EN, HIGH);
  digitalWrite(L_EN, HIGH);
  digitalWrite(relayPin, LOW); // Pastikan relay mati saat mulai

  Serial.begin(9600); // Inisialisasi komunikasi serial dengan kecepatan 9600 bps
}

void loop() {
  // Membaca nilai potensiometer untuk mengatur kecepatan
  potValue = analogRead(potPin);
  motorSpeed = map(potValue, 0, 1023, 0, 255); // Map nilai analog menjadi rentang 0-255 (PWM)

  // Membaca nilai dari sensor infrared
  int obstacleDetected = digitalRead(infraredPin);

  if (obstacleDetected == LOW) { // Jika sensor mendeteksi objek
    digitalWrite(relayPin, HIGH); // Aktifkan relay
    // Hentikan motor
    analogWrite(LPWM, 0);
    analogWrite(RPWM, 0);
    Serial.println("Obstacle detected! Motor stopped.");
  } else {
    digitalWrite(relayPin, LOW); // Matikan relay
    // Mengatur kecepatan motor
    analogWrite(LPWM, motorSpeed);
    analogWrite(RPWM, 0);

    // Menampilkan nilai potensiometer dan kecepatan motor ke Serial Monitor
    Serial.print("Potentiometer Value: ");
    Serial.print(potValue);
    Serial.print(" | Motor Speed: ");
    Serial.println(motorSpeed);
  }

  delay(100); // Delay untuk memperlambat pembacaan potensiometer dan sensor
}
