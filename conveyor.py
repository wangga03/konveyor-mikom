import cv2 as cv
import numpy as np
import time


def main(capture) :

    data1=np.load('/home/wgg/Github/konveyor-mikom/low.npy')
    data2=np.load('/home/wgg/Github/konveyor-mikom/high.npy')

    counter = 0
    lastCounter = 1
    while(True) :
        ret, frame = capture.read()
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        tresh_whiteColor = cv.inRange(hsv, data1, data2)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
        tresh_whiteColor = cv.morphologyEx(tresh_whiteColor, cv.MORPH_OPEN, kernel)

        contour_white,_= cv.findContours(tresh_whiteColor, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        print(len(contour_white))
        
        if 3 <= len(contour_white) <= 10:

            colour = (255,255,255)
            font = cv.FONT_HERSHEY_SIMPLEX

            largest_contours = max(contour_white, key=cv.contourArea)

            x, y, w, h = cv.boundingRect(largest_contours)

            counter+=1
            cv.putText(frame, 'Bata Putih', (x, y+50), font, 1, colour, 2)
            cv.putText(frame, f'Jumlah Bata : {counter}', (100, 100), font, 1, colour, 2)
            cv.rectangle(frame, (x, y), (w + x, h + y), (255,255,255), 2)

        else :
            counter = 0


        cv.imshow("frame", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__' :
    
    cap = cv.VideoCapture(2)    
    main(cap)

