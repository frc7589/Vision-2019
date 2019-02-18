#!/bin/sh

sleep 10
cd $(dirname $0)
./gst-nv3cam0.sh &
./gst-nv3cam1.sh &
./gst-nv3cam2.sh &
./gst-v4l2.sh &
