import cv2
import numpy as np

def nothing(x):
        pass

cap = cv2.VideoCapture(2)

# Mengatur lebar dan tinggi frame
cap.set(3, 640)
cap.set(4, 480)

# Memberi nama window
cv2.namedWindow("trackbars")

# Membuat trackbars
cv2.createTrackbar("H_Low", "trackbars", 0, 255, nothing)
cv2.createTrackbar("S_Low", "trackbars", 0, 255, nothing)
cv2.createTrackbar("V_Low", "trackbars", 0, 255, nothing)
cv2.createTrackbar("H_Up", "trackbars", 255, 255, nothing)
cv2.createTrackbar("S_Up", "trackbars", 255, 255, nothing)
cv2.createTrackbar("V_Up", "trackbars", 255, 255, nothing)

while(True):

    # Mengambil data frame dari kamera
    ret, frame = cap.read()

    # Mengkonversi frame menjadi HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Mendapatkan posisi terakhir dari trackbars
    h_l = cv2.getTrackbarPos("H_Low", "trackbars")
    s_l = cv2.getTrackbarPos("S_Low", "trackbars")
    v_l = cv2.getTrackbarPos("V_Low", "trackbars")
    h_u = cv2.getTrackbarPos("H_Up", "trackbars")
    s_u = cv2.getTrackbarPos("S_Up", "trackbars")
    v_u = cv2.getTrackbarPos("V_Up", "trackbars")

    lower = np.array([h_l,s_l,v_l])
    upper = np.array([h_u,s_u,v_u])

    # Menyimpan data range warna bola
    np.save('low.npy', lower)
    np.save('high.npy', upper)

    # Melakukan thresholding pada frame HSV
    thresholding = cv2.inRange(hsv, lower, upper)

    # Menggambarkan ulang frame
    cv2.imshow('frame',frame)
    # Menggambarkan ulang hasil thresholding
    cv2.imshow('thresholding',thresholding)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()