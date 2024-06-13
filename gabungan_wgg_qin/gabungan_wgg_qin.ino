#include <LiquidCrystal_I2C.h>

// OLED  myOLED(SDA, SCL);
LiquidCrystal_I2C lcd(0x27, 16, 2);  

int RPWM = 10;
int LPWM = 11;
int L_EN = 13;
int R_EN = 12;
int potPin = A1;
int infraredPin = 9; // Pin sensor infrared
int relayPin = 8; // Pin relay
int potValue;
int motorSpeed;

extern uint8_t BigNumbers[];
extern uint8_t SmallFont[];

void setup() {
  lcd.init();
  lcd.backlight();
  // if(!myOLED.begin(SSD1306_128X32))
  //   while(1);
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
  // Serial Comunication ======================================================

  char receivedData[20]; // 20 Maksimum panjang kata yang diharapkan
  int dataIndex = 0;
  bool newDataReceived = false;

  // if (Serial.available() > 0) {
  //       char incomingByte = Serial.read();
  //       if (incomingByte == ' ') { // Jika menerima karakter newline, itu menandakan akhir kata
  //           receivedData[dataIndex] = '\0'; // Menambahkan null terminator untuk menandai akhir string
  //           dataIndex = 0; // Reset indeks untuk menerima kata berikutnya
  //       } else {
  //           receivedData[dataIndex] = incomingByte;
  //           dataIndex++;
  //           if (dataIndex >= 19) { // Jika panjang kata melebihi 19 karakter, batalkan dan reset
  //               dataIndex = 0;
  //           }
  //       }
  // }

  while (Serial.available() > 0) {
        char incomingByte = Serial.read();
        if (incomingByte == ' ') { // Jika menerima karakter spasi, itu menandakan akhir kata
            receivedData[dataIndex] = '\0'; // Menambahkan null terminator untuk menandai akhir string
            dataIndex = 0; // Reset indeks untuk menerima kata berikutnya
            newDataReceived = true; // Mark that new data has been received
        } else {
            receivedData[dataIndex] = incomingByte;
            dataIndex++;
            if (dataIndex >= sizeof(receivedData) - 1) { // Jika panjang kata melebihi panjang maksimal, batalkan dan reset
                dataIndex = 0;
                memset(receivedData, 0, sizeof(receivedData));
            }
        }
    }

    Serial.print("data yang diterima : ");
    Serial.print(receivedData);
    Serial.println();

  if(newDataReceived){


    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print(receivedData);

    // float convert2Float = atof(receivedData);

    // myOLED.setFont(BigNumbers);
    // // myOLED.setFont(SmallFont);
    // myOLED.clrScr();
    // myOLED.printNumF(convert2Float, 0, CENTER, 1);
    // // myOLED.print(receivedData,CENTER, 1);
    // myOLED.update();
  }

  // =====================================================================================

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

  delay(500); // Delay untuk memperlambat pembacaan potensiometer dan sensor
}