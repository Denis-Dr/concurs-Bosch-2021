from flask_opencv_streamer.streamer import Streamer
import cv2
port = 3040
require_login=False
streamer = Streamer(port,require_login)
import time

cap = cv2.VideoCapture('cameraE.avi')
#video_capture=cv2.VideoCapture(0)
streamer.start_streaming()
while True:
	ret,frame = cap.read()
	if not ret:
		print("failed to grab frame")
		break
	#
	if not streamer.is_streaming:
		streamer.start_streaming()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	streamer.update_frame(gray)
	cv2.imshow('image',gray)
	cv2.waitKey(1)
	#time.sleep(3)