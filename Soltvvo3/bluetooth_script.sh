#!/bin/sh

pulseaudio -D
sleep 5  # 適当にウェイト
bluetoothctl << EOF
power on
connect 00:BB:60:5C:58:72
quit
EOF
