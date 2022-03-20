import socket
import sys
import os 
import hashlib
import time
from datetime import datetime

# Crear socket tcp/ip
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

num_conexiones = int(input('Ingrese la cantidad de conexiones que desea atender'))

while (num_conexiones>25 and num_conexiones <= 0):
    num_conexiones = int(input('Ingrese un número válido de conexiones (Entre 0 y 25)'))


# conectar socket al puerto
server_address = ('192.168.37.133', 8888)
print('El %s esta esparando en el puerto %s' % server_address)
sock.bind(server_address)

#archivo a transmitir
filename = input('Ingrese el nombre del archivo a enviar (Prueba_100mb.txt o Prueba_250mb.txt)')
while filename not in ['Prueba_100mb.txt','Prueba_250mb.txt']:
    filename = input('Ingrese un nombre correcto del archivo a enviar')

tamano_archivo = os.path.getsize(filename)

log = open("./logs/servidor-"+' '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+"log.txt", "w")
log.write('Fecha del archivo: '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+'\n')  
log.write('El nombre del archivo es: '+filename+'\n')  

archivo = open(filename, 'rb')
buf = archivo.read(1024)
md5 = hashlib.md5() 

while(buf):
    md5.update(buf)
    buf = archivo.read(1024)

#Saca el hash del archivo
  
# Listen for incoming connections
sock.listen(25)

for i in range(num_conexiones):
    
    #Leemos la primera linea del archivo 
    f = open(filename,'rb')
    l = f.read(1024)
    
    # Espera por una conexion
    print ( 'El servidor esta esparando una conexión')
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