#!/usr/bin/env python
"""
	blink.py
	~~~~~~~~

	Real-time eye and blink detection with OpenCV
	Usage: ./blink.py 

	:author: Taufan Aditya 
"""
import cv2
import motion
import matching as m

def is_eyes(comps, frame):
	tpl_w = 32
	tpl_h = 24
	found = False
	tpl = ()
	# Possible eyes
	if len(comps) == 2:
		# Find reasonable horizontal and vertical distance
		x_dist_ratio = abs(comps[0][0] - comps[1][0]) /comps[0][2]
		y_dist_ratio = abs(comps[0][1] - comps[1][1])
		# Find reasonable width and height comparison
		w_diff = comps[0][2]-comps[1][2]
		h_diff = comps[0][3]-comps[1][3]
		if (2 <= x_dist_ratio <= 5 and y_dist_ratio <= 5) and (-3 < w_diff < 3 and -2 < h_diff < 2):
			found = True
			for x,y,w,h in comps:
				tpl += ((cv2.getRectSubPix(frame, (w+tpl_w,h+tpl_h), (x+w/2,y+h/2))),)

	return found,tpl

def is_blink(comps, ROI):
	blinked = False
	# Get centroid of ROI and evaluate the component position against it
	centroid_x = ROI[0]+(ROI[2]/2)
	centroid_y = ROI[1]+(ROI[3]/2)
	for x,y,w,h in comps:
		if ( x+w > centroid_x > x) and ( y+h > centroid_y > y):
			blinked = True
			break
	return blinked

def find_eyes(tpl, frame):
	threshold = 0.15
	ROI = m.matching(motion.grayify(tpl),motion.grayify(frame),threshold)
	return ROI

def draw_eye(ROI, frame, color):
	x,y,w,h = ROI
	cv2.rectangle(frame, (x,y), (x+w,y+h), color)
	return frame

if __name__ == '__main__':
	wnd_main = "Blink Detection"
	wnd_debug = "Diff VC"
	streaming = True
	debug = False
	init_stage = False
	tracking_stage = False
	usage_text = "'s' Start - 'r' Reset - 'q' Quit"
	locating_text = "Mode : Locating eye..."
	tracking_text = "Mode : Tracking eye..."
	blinked_text = "*Blinked*"
	prev = None
	diff = None
	tpl = ()
	comps = ()
	blink = ()
	color = (0,255,0)
	diff_color = (255,255,0)
	text_color = (0,0,255)
	font = cv2.FONT_HERSHEY_PLAIN
	delay = 0
	# Initialize VideoCapture
	vc,kernel = motion.init(wnd_main)
	while streaming:
		# Register sequenced images and find all connected components
		key,frame = vc.read()
		# Write usage text
		cv2.putText(frame, usage_text, (20,20), font, 1.0, text_color)
		if init_stage:
			diff,contours = motion.get_components(frame, prev, kernel)
			comps = motion.get_moved_components(contours, 5, 5)
			# If not entering tracking_stage yet, try find eyes within contours
			if not contours == None and not tracking_stage:
				cv2.putText(frame, locating_text, (20,220), font, 1.0, text_color)
				tracking_stage,tpl = is_eyes(comps, frame)
		# Get ROI from eye template against current frame
		if tracking_stage:
			cv2.putText(frame, tracking_text, (20,220), font, 1.0, color)
			for eye in tpl:
				ROI = find_eyes(eye,frame)
				if len(ROI) == 4:
					frame = draw_eye(ROI, frame, color)
					diff = draw_eye(ROI, diff, diff_color)
					if is_blink(comps, ROI):
						blink = ROI
						delay = 3
		# Write text if blinked
		if delay > 0 and tracking_stage:
			cv2.putText(frame, blinked_text, (blink[0],blink[1]-2), font, 1.0, text_color, 2)
			delay -= 1
		# Stream the regular frame for main window
		cv2.imshow(wnd_main, frame)
		# Stream the diff frame for debug window
		if not diff == None and debug:
			cv2.imshow(wnd_debug, diff)
		# Save current frame for next process
		prev = frame
		# Force to take the last 8 bits of the integer returned by waitKey
		key = cv2.waitKey(15)
		key = key & 255 if key + 1 else -1
		# [DEV : 'd' to Debug] 'q' to Quit, 'r' to Reset and 's' to Start 
		if key == ord('q'):
			cv2.destroyAllWindows()
			vc.release()
			streaming = False
		elif key == ord('r') and init_stage:
			tracking_stage = False
		elif key == ord('d') and init_stage:
			debug = True
			cv2.namedWindow(wnd_debug)
		elif key == ord('s') and init_stage == False:
			init_stage = True