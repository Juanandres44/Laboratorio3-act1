import socket
import sys
import os 
import hashlib
import time
from datetime import datetime

# Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
num_conn = int(input('Bienvenido al servidor TCP. Por favor ingresar el numero de conexiones que desea atender: '))

while (num_conn <= 0 and num_conn>25):
    num_conn = int(input('Favor ingresar un número válido de conexiones (Entre 0 y 25): '))


#Conectar socket al puerto
serverAddr = ('192.168.37.133', 8888)
print('El %s esta esparando en el puerto %s' % serverAddr)
sock.bind(serverAddr)

#Archivo a enviar
file = input('Cual archivo desea enviar a los clientes? ej: Prueba_100MB.txt o Prueba_250MB.txt ')
while file not in ['Prueba_100MB.txt','Prueba_250MB.txt']:
    file = input('Favor ingresar un nombre correcto del archivo: ')

archivoTam = os.path.getsize(file)

#Crear logs servidor
log = open("./logs/servidor-"+' '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+"log.txt", "w")
log.write('Fecha: '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+'\n')  
log.write('Nombre: '+file+'\n')  
archivo = open(file, 'rb')
buffer = archivo.read(1024)
hashEnc = hashlib.md5() 

while(buffer):
    hashEnc.update(buffer)
    buffer = archivo.read(1024)
  
# Escuchando conexiones
sock.listen(25)

for i in range(num_conn):

    f = open(file,'rb')
    l = f.read(1024)
    
    # Espera por una conexion
    print ( 'El servidor esta a la espera de una conexión')
    connection, client_address = sock.accept()
    start = time.time()
    log.write('Direccion del cliente: '+str(client_address)+'\n')  
    try:
        print ('Conectado', client_address)
        data = connection.recv(32) 
        connection.sendall(b'Finalizado')
        connection.recv(32)
        connection.sendall(bytes(file, 'utf-8'))
        data = connection.recv(32)
        
        print(data.decode('utf-8'))
        if(data.decode('utf-8')== "listo"):
            connection.sendall(bytes(hashEnc.hexdigest(), 'utf-8'))

            #Enviar archivo
            recibido = connection.recv(32)
            if(recibido.decode('utf-8') == 'Hash recibido'):
                while (l):
                    connection.send(l) 
                    l= f.read(1024)
                connection.send(l)

                #Enviar hash
                print('Conexión finalizada exitosamente')
                log.write('Entrega del archivo: Se envio correctamente'+'\n')  
                end = time.time()

        log.write('Tiempo transferencia: '+str(end-start)+'\n')  
            
    finally:
        connection.close()