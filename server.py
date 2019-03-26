#!/usr/bin/python
'''
	orig author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server
'''
import cv2
import numpy as np
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import time
from SocketServer import ThreadingMixIn
from threading import Thread
import os

cap = []
imgBuf = []
fps = 10

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			camId = int(self.path[-6])
			while True:
				try:
					#buf = open(imgPath, 'rb').read()
					self.wfile.write("--jpgboundary\r\n")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(len(imgBuf[camId])))
					self.end_headers()
					self.wfile.write(bytearray(imgBuf[camId]))
					self.wfile.write('\r\n')
					time.sleep(1.0/fps)
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html') or self.path=="/":
			html = open('index.html', 'r').read()
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write(html)
			return

def capturer():
	global imgBuf
	stopCap = False
	while not stopCap:
		for i in range(0,len(cap)):
			rc,img = cap[i].read()
			if not rc:
				continue
			#cv2.imwrite(imgPath, img)
			img = cv2.merge((img[:,:,0]>>3<<3, img[:,:,1]>>3<<3, img[:,:,2]>>3<<3))
			img = cv2.medianBlur(img,3)
			#yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
			#yuv = cv2.merge((yuv[:,:,0]>>2<<2, yuv[:,:,1]>>6<<6, yuv[:,:,2]>>6<<6))
			#yuv = cv2.medianBlur(yuv,3)
			#img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
			r,imgBuf[i] = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 30])
			#open(imgPath, 'wb').write(buf)
		time.sleep(0.03)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
	pass

def openNvCam(sensor_id):
    cap = cv2.VideoCapture("nvcamerasrc sensor-id="+str(sensor_id)+" ! "
                           "nvvidconv ! video/x-raw, format=(string)I420 ! "
                           "videoconvert ! video/x-raw, format=(string)BGR ! "
                           "appsink")
    return cap

def main():
	global cap, imgBuf, imgPath, stopCap
	imgPath = "/tmp/img.mjpg"
	cap.append(openNvCam(0))
	cap.append(openNvCam(1))
	cap.append(openNvCam(2))
	imgBuf = [None] * len(cap)
	Thread(target=capturer).start()
	try:
		server = ThreadingHTTPServer(('0.0.0.0',9090),CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		stopCap = True
		for c in cap:
			c.release()
		server.shutdown()
		os._exit(0)

if __name__ == '__main__':
	main()
