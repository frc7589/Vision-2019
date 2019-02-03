#gst-launch-1.0 v4l2src device=/dev/video1 ! video/x-raw,width=640,height=480 ! xvimagesink
#gst-launch-1.0 v4l2src device=/dev/video1 ! video/x-raw,width=3840,height=2160 ! omxh264enc bitrate=300000 ! 'video/x-h264, stream-format=(string)byte-stream' ! queue max-size-buffers=0 ! h264parse ! rtph264pay ! udpsink host=172.16.21.1 port=5800
gst-launch-1.0 v4l2src device=/dev/video1 ! video/x-raw,width=800,height=600 ! omxh264enc bitrate=300000 ! 'video/x-h264, stream-format=(string)byte-stream' ! queue max-size-buffers=0 ! h264parse ! rtph264pay ! udpsink host=10.75.89.255 port=5801
