#gst-launch-1.0 nvcamerasrc ! nvoverlaysink -e
#gst-launch-1.0 nvcamerasrc fpsRange="30.0 30.0" sensor-id=1 ! 'video/x-raw(memory:NVMM), width=(int)1948, height=(int)1096, format=(string)I420, framerate=(fraction)12/1' ! \
#nvvidconv flip-method=0 ! videoconvert ! 'video/x-raw,format=GRAY8' ! videoconvert ! omxh264enc bitrate=300000 ! 'video/x-h264, stream-format=(string)byte-stream' ! queue max-size-buffers=0 ! h264parse ! rtph264pay ! udpsink host=10.75.89.255 port=5800
gst-launch-1.0 nvcamerasrc fpsRange="3.0 30.0" sensor-id=0 ! 'video/x-raw(memory:NVMM), width=(int)1948, height=(int)1096, format=(string)I420, framerate=(fraction)8/1' ! \
nvvidconv flip-method=0 ! omxh264enc bitrate=200000 ! 'video/x-h264, stream-format=(string)byte-stream' ! queue max-size-buffers=0 ! h264parse ! rtph264pay ! udpsink host=10.75.89.255 port=5800
