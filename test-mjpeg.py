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

capture=None
imgBuf = None
fps = 10

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print self.path
		if self.path.endswith('.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					'''
					rc,img = capture.read()
					if not rc:
						continue
					#imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
					r, buf = cv2.imencode(".jpg",img)
					'''
					#buf = open(imgPath, 'rb').read()
					self.wfile.write("--jpgboundary\r\n")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(len(imgBuf)))
					self.end_headers()
					self.wfile.write(bytearray(imgBuf))
					self.wfile.write('\r\n')
					time.sleep(1.0/fps)
				except KeyboardInterrupt:
					break
			return
		if self.path.endswith('.html') or self.path=="/":
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="cam.mjpg"/>')
			self.wfile.write('</body></html>')
			return

def capturer():
	global imgBuf
	stopCap = False
	while not stopCap:
		rc,img = capture.read()
		if not rc:
			continue
		#cv2.imwrite(imgPath, img)
		img = cv2.merge((img[:,:,0]>>3<<3, img[:,:,1]>>3<<3, img[:,:,2]>>3<<3))
		img = cv2.medianBlur(img,3)
		yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
		#yuv = cv2.merge((yuv[:,:,0]>>2<<2, yuv[:,:,1]>>6<<6, yuv[:,:,2]>>6<<6))
		yuv = cv2.medianBlur(yuv,3)
		img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
		r,imgBuf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 30])
		#open(imgPath, 'wb').write(buf)
		time.sleep(0.03)

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
	pass

def main():
	global capture, imgPath, stopCap
	imgPath = "/tmp/img.mjpg"
	capture = cv2.VideoCapture(0)
	capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
	capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240);
	Thread(target=capturer).start()
	try:
		server = ThreadingHTTPServer(('0.0.0.0',9090),CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		stopCap = True
		capture.release()
		#server.socket.close()
		server.shutdown()
		os._exit(0)

if __name__ == '__main__':
	main()