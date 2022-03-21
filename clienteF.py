import socket
import sys
import hashlib
import threading
import os
from datetime import datetime
import time

num_clientes = int(input('Bienvenido usuario. Por favor ingrese la cantidad de clientes que desea crear: '))

while (num_clientes <= 0 and num_clientes>25 ):
    num_clientes = int(input('Por favor ingresar un número válido: '))


class Main:    
    def __init__(self):
        self.lock = threading.Lock()
    def cliente_funct(self, nombre):
        self.lock.acquire()
        
        # Creacion de logs
        log = open("./logs/"+nombre+' '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+"log.txt", "w")
        self.lock.release()

        # Crear a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conectar socket al puerto. IP de maquina virtual de ubuntu
        server_address = ('192.168.37.133', 8888)
        print('Connectando a %s puerto %s' % server_address)
        sock.connect(server_address)
        file = open("./ArchivosRecibidos/"+nombre+"-prueba-"+str(num_clientes)+".txt", "w")
       
        
        try:
            # Envio de datos
            mensaje = b'Inicio conexion'
            print ( 'Enviando "%s"' % mensaje)
            sock.sendall(mensaje)
        
            confirmacion = sock.recv(32)
            print(confirmacion.decode('utf-8'))

            #Hash
            hashEnc = hashlib.md5()
            if(confirmacion.decode('utf-8') == "ok"):
                sock.sendall(b'Favor ingresar nombre del archivo: ')
                nA = sock.recv(32)
                nombreArchivo = nA.decode('utf-8') 
                log.write('El nombre del archivo es: '+nombreArchivo+'\n')
                print('El nombre del archivo es: '+nombreArchivo+'\n')
                sock.sendall(b'Listo')
                self.lock.acquire()
                hash = sock.recv(32)
                print('Este es el Hash enviado por el servidor TCP: ',hash.decode('utf-8'))
                sock.sendall(b'Hash recibido')
                self.lock.release()
                num_paq=0
                start = time.time()

                while (True):   
                    data = sock.recv(1024)
                    
                    if data:
                        try:
                            file.write(data.decode('utf-8') + os.linesep)
                            hashEnc.update(data)
                            num_paq+=1
                            
                        except:
                            print("Error") 
                            sock.sendall(b'Error al recibir el archivo')
                            break
                        
                    else:
                        print ('Archivo leido')
                        sock.sendall(b'Archivo recibido')
                        break
                end = time.time()
                
                tam = os.path.getsize("./ArchivosRecibidos/"+nombre+"-prueba-"+str(num_clientes)+".txt")
                
                file.close()
                log.write('El tamaño del archivo es: '+str(tam/1000000)+' MB'+'\n')
                log.write('El nombre del cliente es: '+nombre+'\n')
                print("Hash del archivo leido: {0}".format(hashEnc.hexdigest()))
                  
                if(hash.decode('utf-8') == hashEnc.hexdigest()):
                    print("Archivo leido correctamente")
                    log.write('Entrega del archivo exitosa'+'\n')
                else:
                    print("Error al momento de leer el archivo")
                    log.write('Entrega del archivo no exitosa'+'\n')

                log.write('Tiempo de transferencia: '+str(end-start)+ ' segs'+'\n')  
                log.write('Valor total en bytes recibidos: '+str(tam)+'\n')    
                log.write('Numero de paquetes recibidos: '+str(num_paq)+'\n') 
                
                
        finally:
            print ('Cerrando socket')
            sock.close()
            print('Fin')
            log.close()
                   
def Target(c, nombre):
        c.cliente_funct(nombre)



hilo=Main()
for num_cliente in range(num_clientes):
    cliente = threading.Thread(name="Cliente%s" %(num_cliente+1),
                               target=Target,
                               args=(hilo,"Cliente%s" %(num_cliente+1))
                              )
    cliente.start()