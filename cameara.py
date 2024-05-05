import cv2 as cv

def main(camera) :
    while True :
        
        ret, frame = camera.read()
        flip = cv.flip(frame, 1)
        blur = cv.blur(flip,(10, 2))
        cv.imshow("Frame", flip)
        cv.imshow("Frame", blur)
        if cv.waitKey(1) & 0xFF == ord('q') :
            break
    
    camera.release()
    cv.destroyAllWindows()

if __name__ == '__main__' :
    camera = cv.VideoCapture(0)
    
    main(camera)

