#!/usr/bin/python
import socket

addr = socket.gethostbyname(socket.gethostname())

print addr

addr_file = open("address.txt", "w")
addr_file.write(addr + '\n')
addr_file.close()

