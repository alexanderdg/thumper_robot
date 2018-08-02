import time
import socket
import sys
from threading import Thread

HOST = ''
PORT = 50006
s = None
Data = ""
conn = None

class Mysocket:
	def __init__(self):	
		print "Create socket object"
		self.keep_reading = True
		self.connected = False
		self.my_thread = Thread(target=self.readSocket)
		self.my_thread.setDaemon(True)
		self.my_thread.start()
		#self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def close(self):
		if self.my_thread.is_alive():
                        self.keep_reading = False
                        self.my_thread.join()
		print "Close socket communication"


	def readyToConnect(self):
		print "Ready to connect"
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((HOST, PORT))
		self.s.listen(1)
		self.conn, self.addr = self.s.accept()
		print 'Connected by', self.addr
		self.connected = True

	def readSocket(self):
		while self.keep_reading:
			if self.connected:
				data = self.conn.recv(1024)
				if data:
					self.Data = data
                    	time.sleep(0.001)

	def getData(self):
		return self.Data
	
