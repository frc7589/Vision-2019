import cv2

# compile gstreamer-enabled OpenCV with this repo:
# https://github.com/econsystems/opencv_v4l2
'''
cap = cv2.VideoCapture("nvcamerasrc ! "
                       "video/x-raw(memory:NVMM), width=(int)640, height=(int)480, "
                       "format=(string)I420, framerate=(fraction)30/1 ! "
                       "nvvidconv ! video/x-raw, format=(string)I420 ! "
                       "videoconvert ! video/x-raw, format=(string)BGR ! appsink")
'''
cap = cv2.VideoCapture("nvcamerasrc ! "
                       "nvvidconv ! video/x-raw, format=(string)I420 ! "
                       "videoconvert ! video/x-raw, format=(string)BGR ! "
                       " appsink")


while cap:
	ret,img = cap.read()
	if ret:
		cv2.imshow("XD", img)
		key=cv2.waitKey(33)
		if key==ord('q'):
			break
	else:
		break
