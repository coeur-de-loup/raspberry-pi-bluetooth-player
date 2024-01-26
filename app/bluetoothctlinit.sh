#!/usr/bin/expect

spawn bluetoothctl
sleep 2
send "scan on\r"
sleep 6
send "scan off\r"
sleep 5
send "connect B0:F0:0C:0B:C3:8C\r"
#sleep 3
send "exit\r"
expect eof