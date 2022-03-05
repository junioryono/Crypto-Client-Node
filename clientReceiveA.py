from socket import *
import os

clientPort = 15001
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('', clientPort))
print('Client A is Listening...')

while 1:
	message, address = clientSocket.recvfrom(2048)
	modifiedMessage = message.decode().upper()

	if (modifiedMessage == 'TRUE'):
		with open('unconfirmed_T.txt', 'r') as unconfirmed:
			lines = unconfirmed.read()
		unconfirmed.close()

	else:
		tempBalFile = open('temp_T.txt', 'w')
		tempBalFile.write(modifiedMessage)
		tempBalFile.close()

