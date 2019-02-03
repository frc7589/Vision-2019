#gst-launch-1.0 nvcamerasrc ! nvoverlaysink -e
gst-launch-1.0 nvcamerasrc ! omxh264enc bitrate=300000 ! 'video/x-h264, stream-format=(string)byte-stream' ! queue max-size-buffers=0 ! h264parse ! rtph264pay ! udpsink host=10.75.89.255 port=5800
