#include <LCD-I2C.h>
#include <Wire.h>


LCD_I2C lcd(0x27, 16,2);

void setup() {
    Serial.begin(9600);
    lcd.begin();
    lcd.display();
    lcd.backlight();
}

void loop() {
    static char receivedData[20]; // Maksimum panjang kata yang diharapkan
    static int dataIndex = 0;

    if (Serial.available() > 0) {
        char incomingByte = Serial.read();
        if (incomingByte == ' ') { // Jika menerima karakter newline, itu menandakan akhir kata
            receivedData[dataIndex] = '\0'; // Menambahkan null terminator untuk menandai akhir string
            dataIndex = 0; // Reset indeks untuk menerima kata berikutnya
        } else {
            receivedData[dataIndex] = incomingByte;
            dataIndex++;
            if (dataIndex >= 19) { // Jika panjang kata melebihi 19 karakter, batalkan dan reset
                dataIndex = 0;
            }
        }
    }
    Serial.print("Data yang diterima dari Python: ");
    Serial.println(receivedData);
    lcd.clear();
    lcd.print("test");
    lcd.setCursor(0,0);

    delay(500);
}
