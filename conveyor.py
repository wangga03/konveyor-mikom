import cv2 as cv
import numpy as np
import time
import serial

x_start = 100
y_start = 250
x_end = 500
y_end = 480
# arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1) 
def main(capture) :

    width = 640
    height = 480
    capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    colour_green = (0,255,0)
    colour_red = (0,0,255)
    font = cv.FONT_HERSHEY_SIMPLEX
    low_green=np.load('GREEN_low.npy')
    high_green=np.load('GREEN_high.npy')
    low_white=np.load('red_low.npy')
    high_white=np.load('red_high.npy')

		## inisialisasi nilai awal, last counter = 1 hanya sebagai syarat
    counter = 0
    lastCounter = 1
    

    while(True) :
        status = True
		## capture.read() membaca frame dari variabel capture. Ret mengandung nilai boolean
        ret, frame = capture.read()
        # frameCrop = frameCrop[y_start:y_end, x_start:x_end]

        frame = frame[y_start:y_end, x_start:x_end]

		## cv.cvtColor() digunakan untuk convert warna, dari BGR ke HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

		## Setahu saya untuk fungsinya seperti masking berdasarkan warna pada Photo editing
        tresh_greenColor = cv.inRange(hsv, low_green, high_green)
        tresh_whiteColor = cv.inRange(hsv, low_white, high_white)

        tresh_whiteColor = tresh_whiteColor[y_start:y_end, x_start:x_end]
        tresh_greenColor = tresh_greenColor[y_start:y_end, x_start:x_end]

        ## Invert detection

        _, thress = cv.threshold(tresh_greenColor, 220, 255, cv.THRESH_BINARY_INV)

		## ====
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))

		## ====
        tresh_green = cv.morphologyEx(thress, cv.MORPH_OPEN, kernel)
        tresh_white = cv.morphologyEx(tresh_whiteColor, cv.MORPH_OPEN, kernel)

        contour_green,_= cv.findContours(tresh_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contour_white,_= cv.findContours(tresh_white, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        print(len(contour_green))

        if 2 <= len(contour_white) <= 10 :
            largest_contours_white = max(contour_white, key=cv.contourArea)

            x, y, w, h = cv.boundingRect(largest_contours_white)

            cv.rectangle(frame, (x, y), (w + x, h + y), colour_red, 2)
            status = False
            # print("\n============\nColor White Detected\n===========\n")
        
        if 2 <= len(contour_green) <= 50:


            largest_contours = max(contour_green, key=cv.contourArea)

            x, y, w, h = cv.boundingRect(largest_contours)

            if lastCounter == counter :
                counter+=1
            counterToArduino = str(f"{lastCounter} ")
            # arduino.write(counterToArduino.encode())
            cv.putText(frame, 'Bata Hitam', (x, y+50), font, 1, colour_green, 2)
            cv.rectangle(frame, (x, y), (w + x, h + y), colour_green, 2)

        else :
            if status == True :
                lastCounter = counter

		## Menampilkan window untuk frame
        cv.putText(frame, f'Jumlah Bata : {lastCounter}', (100, 100), font, 1, colour_green, 2)
        cv.imshow("frame", hsv)
        # cv.imshow("frame crop", frameCrop)
        cv.imshow("tresh green", tresh_green)
        cv.imshow("tresh white", tresh_white)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__' :
    
		## Membaca aliran data dari camera,0 merupakan index camera. Index camera tidak selalu 0
    cap = cv.VideoCapture(2)    
    
    main(cap)

