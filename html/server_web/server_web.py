import socket

# creeaza un server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# specifica ca serverul va rula pe portul 5678, accesibil de pe orice ip al serverului
serversocket.bind(('', 5678))
# serverul poate accepta conexiuni; specifica cati clienti pot astepta la coada
serversocket.listen(5)

while True:
	print ('#########################################################################')
	print ('Serverul asculta potentiali clienti.')
	# asteapta conectarea unui client la server
	# metoda `accept` este blocanta => clientsocket, care reprezinta socket-ul corespunzator clientului conectat
	(clientsocket, address) = serversocket.accept()
	print ('S-a conectat un client.')
	# se proceseaza cererea si se citeste prima linie de text
	cerere = ''
	linieDeStart = ''
	while True:
		buf = clientsocket.recv(1024)
		if len(buf) < 1:
			break
		cerere = buf.decode()
		print ('S-a citit mesajul: \n---------------------------\n' + cerere + '\n---------------------------')
		pozitie = cerere.find('\r\n')
		if (pozitie > -1 and linieDeStart == ''):
			linieDeStart = cerere[0:pozitie]
			print ('S-a citit linia de start din cerere: ##### ' + linieDeStart + ' #####')
			break
	print ('S-a terminat cititrea.')
	if linieDeStart == '':
		clientsocket.close()
		print ('S-a terminat comunicarea cu clientul - nu s-a primit niciun mesaj.')
		continue
	# interpretarea sirului de caractere `linieDeStart`
	elementeLineDeStart = linieDeStart.split(' ')
	# TODO securizare
	numeResursaCeruta = elementeLineDeStart[1]
	
	# calea este relativa la directorul de unde a fost executat scriptul
	numeFisier = 'continut' + numeResursaCeruta

	try:
		# deschide fisierul pentru citire in mod binar
		fisier = open(numeFisier,'rb').read()
		content = ''
		# tip media
		numeExtensie = numeFisier.split('.')[1]
		if numeExtensie in ['html', 'css', 'xml']:
			content = 'text/' + numeExtensie
		elif numeExtensie in ['png', 'jpeg', 'gif']:
			content = 'image/' + numeExtensie
		elif numeExtensie == 'js':
			content = 'application/javascript'
		elif numeExtensie == 'jpg':
			content = 'image/jpeg'
		elif numeExtensie == 'ico':
			content == 'image/x-icon'
		
		# se trimite raspunsul
		clientsocket.sendall(('HTTP/1.1 200 OK\r\n').encode('UTF-8'))
		clientsocket.sendall(('Content-Length: ' + str(os.stat(numeFisier).st_size) + '\r\n').encode('UTF-8'))
		clientsocket.sendall(('Content-Type: ' + content +'\r\n').encode('UTF-8'))
		clientsocket.sendall(('Server: My PW Server\r\n').encode('UTF-8'))
		clientsocket.sendall(('\r\n').encode('UTF-8'))
		clientsocket.sendall(fisier)
	
	except IOError:
		# daca fisierul nu exista trebuie trimis un mesaj de 404 Not Found
		msg = 'Eroare! Resursa ceruta ' + numeResursaCeruta + ' nu a putut fi gasita!'
		print (msg)
		clientsocket.sendall(('HTTP/1.1 404 Not Found\r\n').encode('UTF-8'))
		clientsocket.sendall(('Content-Length: ' + str(len(msg)) + '\r\n').encode('UTF-8'))
		clientsocket.sendall(('Content-Type: text/html\r\n').encode('UTF-8'))
		clientsocket.sendall(('Server: My PW Server\r\n').encode('UTF-8'))
		clientsocket.sendall(('\r\n').encode('UTF-8'))
		clientsocket.sendall((msg).encode('UTF-8'))

	finally:
		clientsocket.close()
	print ('S-a terminat comunicarea cu clientul.')
