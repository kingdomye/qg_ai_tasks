import cv2 as cv
import numpy as np

img = cv.imread("imgs/sudok.jpg")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 150, apertureSize=3)
lines = cv.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=30)

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

cv.imshow('res', img)
cv.waitKey(0)
cv.destroyAllWindows()
