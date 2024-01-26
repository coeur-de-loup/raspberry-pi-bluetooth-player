#!/usr/bin/expect

spawn bluetoothctl
sleep 2
send "exit\r"
expect eof