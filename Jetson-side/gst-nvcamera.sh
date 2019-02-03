#gst-launch-1.0 nvcamerasrc ! nvoverlaysink -e
gst-launch-1.0 nvcamerasrc ! omxh264enc bitrate=7000000 ! 'video/x-h264, stream-format=(string)byte-stream' ! queue max-size-buffers=0 ! h264parse ! rtph264pay ! udpsink host=224.1.1.1 auto-multicast=true port=5800
