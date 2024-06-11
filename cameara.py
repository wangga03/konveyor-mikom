import cv2

# Membuka kamera (atau video file)
cap = cv2.VideoCapture(0)  # 0 untuk webcam default

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Menentukan koordinat untuk crop
    x_start = 100
    y_start = 50
    x_end = 400
    y_end = 300

    # Melakukan crop
    cropped_frame = frame[y_start:y_end, x_start:x_end]

    # Menampilkan frame yang sudah dipotong
    cv2.imshow('Cropped Frame', cropped_frame)

    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Membersihkan dan menutup jendela
cap.release()
cv2.destroyAllWindows()
