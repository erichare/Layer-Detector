#! /usr/bin/env python

import sys
import cv
from itertools import izip

# some definitions
win_name = "Edge"

# definition of some colors
_red =  (0, 0, 255, 0);
_green =  (0, 255, 0, 0);
_white = cv.RealScalar (255)
_black = cv.RealScalar (0)

num_points = 0
num_points_prev = 0
f = open('edge_results.txt', 'a')
def processClick(event, x, y, flags, param):
	if (event == cv.CV_EVENT_LBUTTONDOWN):
		cv.DestroyWindow("Original")
		lst = []
		for i in range(y, edge.height):
			val = cv.Get2D(edge, i, x)[0]
			if val > 0:
				lst.append((x, i))

		for i in lst:
			cv.Circle(edge, i, 3, (255, 255, 255), thickness = -1)
			font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.3, 0.3)
			cv.PutText(edge, str(i[1]), i, font, (255, 255, 255))

		num_points = len(lst)
		cv.ShowImage(win_name, edge)

		f.write("=========================\n")
		f.write("X Coordinate: " + str(x) + "\n")
		
		count = 0
		prev = None
		i = 0
		j = 0
		while i < len(lst):
			pt = lst[i]
			if (j % 2 == 1):
				count = count + 1
				f.write("Edge " + str(count) +": top = " + str(prev[1]) + ", bottom = " + str(pt[1]) + ", width = " + str(pt[1] - prev[1]) + "\n")
			elif (i < len(lst) - 3 and lst[i + 2][1] - pt[1] <= 25):
				i = i + 1
				
			prev = lst[i]
			i = i + 1
			j = j + 1
			
		f.write("=========================\n\n")

		num_points_prev = num_points
		cv.WaitKey(0)
		f.close()

im = cv.LoadImage(sys.argv[1], cv.CV_LOAD_IMAGE_COLOR)
f.write("Image File: " + sys.argv[1])

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
cv.SetMouseCallback("Original", processClick, None)
cv.SetMouseCallback(win_name, processClick, None)
cv.WaitKey(0)
