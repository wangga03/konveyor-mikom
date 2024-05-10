void setup() {
    Serial.begin(9600);
}

void loop() {
    static char receivedData[20]; // Maksimum panjang kata yang diharapkan
    static int dataIndex = 0;

    if (Serial.available() > 0) {
        char incomingByte = Serial.read();
        if (incomingByte == ' ') { // Jika menerima karakter newline, itu menandakan akhir kata
            receivedData[dataIndex] = '\0'; // Menambahkan null terminator untuk menandai akhir string
            Serial.print("Data yang diterima dari Python: ");
            Serial.println(receivedData);
            dataIndex = 0; // Reset indeks untuk menerima kata berikutnya
        } else {
            receivedData[dataIndex] = incomingByte;
            dataIndex++;
            if (dataIndex >= 19) { // Jika panjang kata melebihi 19 karakter, batalkan dan reset
                dataIndex = 0;
            }
        }
    }
}
