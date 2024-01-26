#!/usr/bin/expect

spawn bluetoothctl
sleep 10
send "exit\r"
expect eof