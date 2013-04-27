#!/usr/bin/env python
"""
    detect.py
    ~~~~~~~~~

	Face-detection with OpenCV

	Usage: ./detect.py some-picture.jpg 
	(Will outputing "some-picture-output.jpg" with rectangled faces)

    :author: Taufan Aditya 
"""
import cv2
import sys

def detect(img,out): 
	color = (0,255,0)
	cascade = cv2.CascadeClassifier("res/haarcascade_frontalface_alt.xml")
	faces = cascade.detectMultiScale(img, 1.2, 2, 0, (100,100))
	if (faces == None):
		print "None found!"
	else:
		print len(faces)," found!"
		# w=width, h=height
		for (x,y,w,h) in faces:
			cv2.rectangle(img, (x,y), (x+w,y+h), color)

		cv2.imwrite(out,img)
		print "See :", out

if __name__ == '__main__':
	infile = str(sys.argv[len(sys.argv)-1])
	img = cv2.imread(infile);
	# imread function will returned nothing if fail
	if (img == None):
		print "Thats not a file"
	else:
		print "Detecting faces within :", infile
		detect(img,"-output.".join(infile.split(".")))