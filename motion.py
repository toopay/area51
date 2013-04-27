#!/usr/bin/env python
"""
	motion.py
	~~~~~~~~~

	Motion detector with OpenCV 

	Usage: ./motion.py 
	(Press 's' to start tracking and 'q' to Quit)

	:author: Taufan Aditya 
"""
import cv2

def init(video): 
	vc = cv2.VideoCapture(0)
	if not vc.isOpened():
		print "Cannot open device!"
		return
	# Set the vc to 320x240
	vc.set(3, 320) 
	vc.set(4, 240)
	cv2.namedWindow(video)
	# Set initial kernel for morphology transformation
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
	return (vc,kernel)
	
def grayify(img):
	return cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

def get_components(frame, prev, kernel, video):
	# Stream diff frame for secondary window
	diff = cv2.subtract(grayify(frame), grayify(prev));
	(thresh, diff) = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)
	diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel)
	cv2.imshow(video, diff)
	# Find contours and hierarcy from diff
	(contours, hierarchy) = cv2.findContours(diff, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	return contours

def draw_motion(contours, frame):
	for c in contours:
		(x,y,w,h) = cv2.boundingRect(c)
		# Optimize the motion result by reduce the noise
		if w > 5 and h > 5:
			cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0))
	return frame

if __name__ == '__main__':
	init_stage = False
	wnd_main = "Main VC"
	wnd_debug = "Diff VC"
	prev = None
	# Initialize VideoCapture 
	(vc,kernel) = init(wnd_main)
	while True:
		val,frame = vc.read()
		if init_stage:
			contours = get_components(frame, prev, kernel, wnd_debug)
			if not contours == None:
				frame = draw_motion(contours, frame)

		# Stream the frame for main window
		cv2.imshow(wnd_main, frame)
		prev = frame
		# Force to take the last 8 bits of the integer returned by waitKey
		key = cv2.waitKey(15)
		key = key & 255 if key + 1 else -1
		# 'q' to Quit and 's' to Start 
		if key == ord('q'):
			cv2.destroyAllWindows()
			vc.release()
			break
		elif key == ord('s') and init_stage == False:
			cv2.namedWindow(wnd_debug)
			init_stage = True