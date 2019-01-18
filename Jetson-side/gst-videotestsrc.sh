gst-launch-1.0 videotestsrc ! omxh264enc bitrate=300000 ! 'video/x-h264, stream-format=(string)byte-stream' ! queue max-size-buffers=0 ! h264parse ! rtph264pay ! udpsink host=172.16.21.1 port=5800
