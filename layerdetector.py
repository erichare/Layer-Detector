#! /usr/bin/env python

import sys
import cv

# some definitions
win_name = "Edge"

# definition of some colors
_red =  (0, 0, 255, 0);
_green =  (0, 255, 0, 0);
_white = cv.RealScalar (255)
_black = cv.RealScalar (0)

im = cv.LoadImage(sys.argv[1], cv.CV_LOAD_IMAGE_COLOR)

# create the output im
col_edge = cv.CreateImage((im.width, im.height), 8, 3)

# convert to grayscale
gray = cv.CreateImage((im.width, im.height), 8, 1)
edge = cv.CreateImage((im.width, im.height), 8, 1)
cv.CvtColor(im, gray, cv.CV_BGR2GRAY)

# create the window
cv.NamedWindow(win_name, cv.CV_WINDOW_AUTOSIZE)

# show the im
cv.Smooth(gray, edge, cv.CV_BLUR, 3, 3, 0)
cv.Not(gray, edge)

# run the edge dector on gray scale
threshold = 100
cv.Canny(gray, edge, threshold, threshold * 3, 3)

# copy edge points
cv.Copy(im, col_edge, edge)

# show the im
cv.ShowImage("Original", im)

cv.WaitKey(0)
cv.DestroyWindow("Original")

lst = []
x = edge.width / 4
for i in range(edge.height):
	val = cv.Get2D(edge, i, x)[0]
	if val > 0:
		lst.append((x, i))

for i in lst:
	cv.Circle(edge, i, 3, (255, 255, 255), thickness = -1)
	font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.3, 0.3)
	cv.PutText(edge, str(i[1]), i, font, (255, 255, 255))

cv.ShowImage(win_name, edge)

cv.WaitKey(0)
