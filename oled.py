import smbus2
import time

# Alamat I2C layar OLED (pastikan ini sesuai dengan alamat layar Anda)
DEVICE_ADDRESS = 0x3C

# Inisialisasi bus I2C
bus = smbus2.SMBus(1)

# Fungsi untuk mengirimkan byte tunggal ke layar OLED
def send_byte(byte):
    bus.write_byte(DEVICE_ADDRESS, byte)

# Fungsi untuk mengirimkan data ke layar OLED
def send_data(data):
    bus.write_byte_data(DEVICE_ADDRESS, 0x40, data)

# Fungsi untuk membersihkan layar OLED
def clear_display():
    send_byte(0x00)
    send_byte(0x10)

# Fungsi untuk menulis teks pada layar OLED
def write_text(text):
    for char in text:
        send_data(ord(char))

# Bersihkan layar OLED
clear_display()

# Tulis teks pada layar OLED
write_text("Hello, OLED!")

# Tunggu beberapa saat sebelum menutup program
time.sleep(5)

