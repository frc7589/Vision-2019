gst-launch-1.0 -vvv -e udpsrc port=$1 ! "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtph264depay ! avdec_h264 ! autovideosink
