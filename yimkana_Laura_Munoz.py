#!/usr/bin/python3 -u

#Laura Muñoz Jávega, Práctica Redes de Computadores II 2019/2020

from socket import socket,AF_INET, SOCK_STREAM, SOCK_DGRAM 
import hashlib, binascii, struct, base64

###################____RETO 0____############################
def yimkana0():
	
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect(('node1',2000))
	print(sock.recv(1200).decode())
	
	
	sock.send('laura.munoz23'.encode())
	
	
	msg = sock.recv(1200).decode()
	print(msg)
	
	
	sock.close()
	
	
	identificador = msg.split('\n')[0] 
	    
	return identificador

###################____RETO 1____############################
def yimkana1(identificador):
	
	sockcli = socket(AF_INET, SOCK_DGRAM) #socket cliente
	sockser = socket(AF_INET, SOCK_DGRAM) #socket servidor
	
	
	sockser.bind(('',1875))  
	
	
	msg_iden = (str('1875')+' '+str(identificador))
	sockcli.sendto(msg_iden.encode(),('node1',3000)) 
	
	
	msg = sockser.recv(1200).decode() 
	print(msg) 
	
	
	sockcli.close() 
	sockser.close() 

	
	ident = msg.split('\n')[0] 
	ident1 = ident.split(':',2)[1] 
	
	return ident1

###################____RETO 2____############################
def yimkana2(ident):
	
	sock = socket(AF_INET,SOCK_STREAM)
	sock.connect(('node1',4001))
	
	msg = ''
	CONT = 0
	
	while True:
		datos_recv = sock.recv(32).decode()
		msg+= datos_recv
		if datos_recv.find(' 0 ')!= -1:
			break
	
	conjuntoNumeros = msg.split()
	while CONT < len(conjuntoNumeros):
		numero = conjuntoNumeros[CONT]
		if numero =='0':
			print("Se ha encontrado el 0 en la secuencia, en la posicion:", CONT)
			break
		CONT+=1
	
	print("La cantidad de numeros es",CONT)
	print()

	msg_iden = (ident+' '+str(CONT))
	sock.send(msg_iden.encode())
	
	while True:
		datos = sock.recv(1024).decode()
		if ">" in datos:
			print(datos)
			break
	
	sock.close()
	
	ident2 = datos.split('\n')[0]
	ident3 = ident2.split(':',2)[1]
	
	return ident3

###################____RETO 3____############################


def recibirTodo(sock):
	datos = ''
	while True:
		pequeño = sock.recv(32).decode()
		datos += pequeño
		if hayPalindromo(pequeño) == True:
			break;
	return datos


def hayPalindromo(dato):
	palindromo = False
	listadato = dato.split()
	for i in range(0,len(listadato)):
		if len(listadato[i]) <= 1 or listadato[i].isdigit():
			break;
		palindromo = esPalindromo(listadato[i])
		if palindromo == True:
			break;
	return palindromo	
	
def esPalindromo(pal):
	esPal = pal.lower()
	return esPal == esPal[::-1]

def yimkana3(ident2):
	msg = ''
	igual = 0
	aux = 0
	
	sock = socket(AF_INET,SOCK_STREAM)
	sock.connect(('node1',6000))
	
	datos = recibirTodo(sock)
	listaNormal = datos.split()
	listaReves = []
	
	for i in range(0,len(listaNormal)):
		palabra = str(listaNormal[i]).lower()
		if palabra == palabra[::-1] and len(palabra) >= 2 and palabra.isdigit() == False:
			break
		if palabra.isdigit():
			listaReves.append(listaNormal[i]) 
		else:
			listaReves.append(listaNormal[i][::-1]) 
	
	cadena =' '.join(listaReves)
	
	print('Mensaje invertido: ',cadena)
	sock.send(cadena.encode())
	msg_iden1 = ('--'+ident2+'--')
	sock.send(msg_iden1.encode())
	
	while True:
		datos = sock.recv(1024).decode()
		if ">" in datos:
			print(datos) 
			break
	
	sock.close()

	ident2 = datos.split('\n')[0]
	ident3 = ident2.split(':',1)[1]
	return ident3

###################____RETO 4____############################
def yimkana4(ident3):

	sock = socket(AF_INET,SOCK_STREAM)
	sock.connect(('node1',10001))
	
	msg_id3 = ident3.encode()
	sock.send(msg_id3)
	
	primero = False 
	while 1:
		datos_recv = sock.recv(1024)
		
		if( primero == False):
			total = datos_recv.split(b':',1)
			primero = True
			parteUno= total[0].decode()
			parteUno = int(parteUno)
			parteDos = total[1]
			print('Bytes del principio:', parteUno)
			msgtotal=parteDos
			
			
		else:
			msgtotal += datos_recv
			if(len(msgtotal) == parteUno):
				print('Bytes del final:',len(msgtotal)) 

				break;
		
	resultado = hashlib.sha1(msgtotal)
	
	print('El hexadecimal equivalente:')
	equivalente = resultado.hexdigest()
	print(equivalente)
	
	equivalente_binario = binascii.unhexlify(equivalente)
	sock.send(equivalente_binario)
	
	while True:
		datos2 = sock.recv(2048).decode()
		if ">" in datos2:
			print(datos2) 
			break
	
	
	sock.close()
	ident = datos2.split('\n')[0]
	ident4 = ident.split(':',1)[1]
	return ident4

###################RETO5#############################

# Copyright (C) 2009-2020  David Villa Alises
def sum16(data):
    if len(data) % 2:
        data = b'\0' + data

    return sum(struct.unpack('!%sH' % (len(data) // 2), data))


def cksum(data):
	sum_as_16b_words  = sum16(data)
	sum_1s_complement = sum16(struct.pack('!L', sum_as_16b_words))
	_1s_complement    = ~sum_1s_complement & 0xffff
	return _1s_complement


def yimkana5(ident4):
	
	cabecera_format = '!3sBHH'      
	sock = socket(AF_INET, SOCK_DGRAM) 
	
	payload = base64.b64encode(ident4.encode())
	header = struct.pack(cabecera_format,b'WYP',0, 0,0)+payload
	
	check = cksum(header)
	print('Primer checksum:',check)

	header1 = struct.pack(cabecera_format,b'WYP',0, 0, check)+payload
	check1 = cksum(header1)
	print('Segundo checksum:',check1)
	print('Cabecera que enviamos-->',header1)

	sock.sendto(header1,('node1',7001)) 

	datos2, servidor = sock.recvfrom(2048) 
	longitud_msg = str(len(datos2)-8)
	formato_msg = '!3sBHH'+longitud_msg+'s'
	reto6_pte1= struct.unpack(formato_msg, datos2)
	reto6_pte1 = base64.b64decode(reto6_pte1[4])
	print(reto6_pte1.decode()) 
			
	sock.close()


identificador = yimkana0() 
ident = yimkana1(identificador) 
ident2 = yimkana2(ident)
ident3 = yimkana3(ident2)
ident4 = yimkana4(ident3)
yimkana5(ident4)


