from socket import *

clientReceivePort = 15000
clientReceiveSocket = socket(AF_INET, SOCK_DGRAM)
clientReceiveSocket.bind(('', clientReceivePort))

clientSendName = 'localhost'
clientSendPort = 15001
clientSendSocket = socket(AF_INET, SOCK_DGRAM)

fullNodeReceivePort = 13001
fullNodeReceiveSocket = socket(AF_INET, SOCK_DGRAM)
fullNodeReceiveSocket.bind(('', fullNodeReceivePort))

fullNodeSendName = 'localhost'
fullNodeSendPort = 13000
fullNodeSendSocket = socket(AF_INET, SOCK_DGRAM)

transactionFee = 2
miningFee = 30 
fullNodeBalance = 0

print('Full Node A Listening...')

while 1: 
	message, clientAddress = clientReceiveSocket.recvfrom(2048)
	messageDecoded = message.decode()

	if (messageDecoded[0] == 'C'):
		fullNodeSendSocket.sendto(str.encode(str('F' + messageDecoded[1:]), 'utf-8'), (fullNodeSendName, fullNodeSendPort))

		message2, clientAddress2 = fullNodeReceiveSocket.recvfrom(2048)
		messageDecoded2 = message2.decode()
		
		if (messageDecoded2[0] == 'F'):
			messageDecoded2 = messageDecoded2[1:]
			clientSendSocket.sendto(messageDecoded2.encode(), (clientSendName, clientSendPort))