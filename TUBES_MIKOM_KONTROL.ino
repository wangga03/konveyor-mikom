int RPWM = 5;
int LPWM = 6;
int L_EN = 3;
int R_EN = 2;
int potPin = A2; 
int potValue;
int motorSpeed;

void setup() {
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);
  pinMode(potPin, INPUT);
  digitalWrite(R_EN, HIGH);
  digitalWrite(L_EN, HIGH);
  Serial.begin(9600); // Inisialisasi komunikasi serial dengan kecepatan 9600 bps
}

void loop() {
  // Membaca nilai potensiometer untuk mengatur kecepatan
  potValue = analogRead(potPin);
  motorSpeed = map(potValue, 0, 1023, 0, 255); // Map nilai analog menjadi rentang 0-255 (PWM)

  // Mengatur kecepatan motor
  analogWrite(LPWM, motorSpeed);
  analogWrite(RPWM, 0);

  // Menampilkan nilai potensiometer dan kecepatan motor ke Serial Monitor
  Serial.print("Potentiometer Value: ");
  Serial.print(potValue);
  Serial.print(" | Motor Speed: ");
  Serial.println(motorSpeed);
  delay(100); // Delay untuk memperlambat pembacaan potensiometer
  
}
