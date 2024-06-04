import cv2 as cv
import numpy as np
import time
import serial


# arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1) 
def main(capture) :
    low=np.load('low.npy')
    high=np.load('high.npy')

		## inisialisasi nilai awal, last counter = 1 hanya sebagai syarat
    counter = 0
    lastCounter = 1

    while(True) :
					## capture.read() membaca frame dari variabel capture. Ret mengandung nilai boolean
        ret, frame = capture.read()

					## cv.cvtColor() digunakan untuk convert warna, dari BGR ke HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

					## Setahu saya untuk fungsinya seperti masing berdasarkan warna pada Photo editing
        tresh_whiteColor = cv.inRange(hsv, low, high)

					## ====
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))

					## ====
        tresh_whiteColor = cv.morphologyEx(tresh_whiteColor, cv.MORPH_OPEN, kernel)

        contour_white,_= cv.findContours(tresh_whiteColor, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        print(len(contour_white))
        
        if 2 <= len(contour_white) <= 10:

            colour = (0,255,255)
            font = cv.FONT_HERSHEY_SIMPLEX

            largest_contours = max(contour_white, key=cv.contourArea)

            x, y, w, h = cv.boundingRect(largest_contours)

            if lastCounter == counter :
                counter+=1
            counterToArduino = str(f"{lastCounter} ")
            # arduino.write(counterToArduino.encode())
            cv.putText(frame, 'Bata Putih', (x, y+50), font, 1, colour, 2)
            cv.putText(frame, f'Jumlah Bata : {lastCounter}', (100, 100), font, 1, colour, 2)
            cv.rectangle(frame, (x, y), (w + x, h + y), (0,255,255), 2)

        else :

            lastCounter = counter

					## Menampilkan window untuk frame
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

