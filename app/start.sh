#!/bin/bash
expect /home/pi/btplayer/app/bluetoothctlinit.sh

sleep 10
exec "$@"
