#!/usr/bin/env python
"""
	matching.py
	~~~~~~~~~~~

	Template matching with OpenCV 

	Usage: ./matching.py main-image.jpg template-image.jpg 
	(Will outputing "main-image-match.jpg" with rectangled ROI)

	:author: Taufan Aditya 
"""
import cv2

def matching(tpl,img,treshold): 
	try:
		ROI = ()
		result = cv2.matchTemplate(tpl,img,cv2.TM_SQDIFF_NORMED)
		min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
		if min_val <= treshold:
			# Match enough
			ROI = min_loc+(len(tpl[0]),len(tpl))

		return ROI
	except:
		return ()

if __name__ == '__main__':
	import sys
	if len(sys.argv) < 3 :
		sys.stderr.write("Usage : ./matching.py main-image.jpg template-image.jpg")
	else:
		mainfile = str(sys.argv[len(sys.argv)-2])
		img = cv2.imread(mainfile);
		tplfile = str(sys.argv[len(sys.argv)-1])
		tpl = cv2.imread(tplfile);
		# imread function will returned nothing if fail
		if img == None or tpl == None:
			print "Thats not a file"
		else:
			print "Detecting ROI within :", mainfile, ", with template :", tplfile
			ROI = matching(tpl,img,0.4)

			if len(ROI) == 4:
				out = "-match.".join(mainfile.split("."))
				cv2.rectangle(img, (ROI[0],ROI[1]), (ROI[0]+ROI[2],ROI[1]+ROI[3]), (0,255,0))
				cv2.imwrite(out,img)
				print "See :", out
			else:
				print "None found!"