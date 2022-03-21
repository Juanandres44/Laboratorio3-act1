import socket
import sys
import os 
import hashlib
import time
from datetime import datetime

# Crear socket tcp/ip
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

num_conn = int(input('Bienvenido al servidor TCP. Por favor ingresar la cantidad de conexiones: '))

while (num_conn>25 and num_conn <= 0):
    num_conn = int(input('Por favor ingresar un número válido: '))


# conectar socket al puerto
server_address = ('192.168.37.133', 8888)
print('El %s esta esparando en el puerto %s' % server_address)
sock.bind(server_address)

#archivo a transmitir
filename = input('Por favor ingrese el nombre del archivo a enviar. ej: Prueba_100MB.txt o Prueba_250MB.txt')
while filename not in ['Prueba_100MB.txt','Prueba_250MB.txt']:
    filename = input('Por favor ingresar un nombre de archivo correcto: ')

tamano_archivo = os.path.getsize(filename)

log = open("./logs/servidor-"+' '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+"log.txt", "w")
log.write('Fecha: '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+'\n')  
log.write('El nombre es: '+filename+'\n')  

archivo = open(filename, 'rb')
buf = archivo.read(1024)
md5 = hashlib.md5() 

while(buf):
    md5.update(buf)
    buf = archivo.read(1024)

  
sock.listen(25)

for i in range(num_conn):

    f = open(filename,'rb')
    l = f.read(1024)
  
    print ( 'El servidor esta a la espera de una conexión')
    connection, client_address = sock.accept()
    start = time.time()
    log.write('Direccion del cliente: '+str(client_address)+'\n')  
    try:
        print ( 'Conectado desde', client_address)
        
        data = connection.recv(32) 
            
        connection.sendall(b'ok')
        
        connection.recv(32)
        connection.sendall(bytes(filename, 'utf-8'))
        
        data = connection.recv(32)
        
        print(data.decode('utf-8'))
        # Recibir datos y retransmitirlos
       
        if(data.decode('utf-8')== "listo"):
            
            connection.sendall(bytes(md5.hexdigest(), 'utf-8'))
            #Enviamos linea por linea el archivo
            recibido = connection.recv(32)
            if(recibido.decode('utf-8') == 'Hash recibido'):
                while (l):
                    connection.send(l) 
                    l= f.read(1024)
            
                connection.send(l)
                #Enviamos el hash
                print('Conexión terminada exitosamente')
                log.write('Entrega del archivo: se envio el archivo '+'\n')  
                end = time.time()

        log.write('Tiempo transferencia con cliente: '+str(end-start)+'\n')  
            
    finally:
        # cerrar coneccion
        connection.close()