import cv2 as cv
import numpy as np
import time
import serial


# arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1) 
def main(capture) :
    colour_green = (0,255,0)
    colour_red = (0,0,255)
    font = cv.FONT_HERSHEY_SIMPLEX
    low_green=np.load('conveyor_belt_low.npy')
    high_green=np.load('conveyor_belt_high.npy')
    low_white=np.load('white_low.npy')
    high_white=np.load('white_high.npy')

		## inisialisasi nilai awal, last counter = 1 hanya sebagai syarat
    counter = 0
    lastCounter = 1
    

    while(True) :
        status = True
		## capture.read() membaca frame dari variabel capture. Ret mengandung nilai boolean
        ret, frame = capture.read()

		## cv.cvtColor() digunakan untuk convert warna, dari BGR ke HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

		## Setahu saya untuk fungsinya seperti masking berdasarkan warna pada Photo editing
        tresh_greenColor = cv.inRange(hsv, low_green, high_green)
        tresh_whiteColor = cv.inRange(hsv, low_white, high_white)

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
            print("\n============\nColor White Detected\n===========\n")
        
        if 2 <= len(contour_green) <= 10:


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
        cv.imshow("frame", frame)
        cv.imshow("tresh", tresh_whiteColor)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__' :
    
		## Membaca aliran data dari camera,0 merupakan index camera. Index camera tidak selalu 0
    cap = cv.VideoCapture(0)    
    
    main(cap)

