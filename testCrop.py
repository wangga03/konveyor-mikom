import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('Screenshot from 2024-05-27 11-04-29.png')
row, cols, _ = img.shape

print("rows", row)
print("cols", cols)

cut = img[0: 200, 300: 300]

cv.imshow("aa",cut)
cv.waitKey(0)