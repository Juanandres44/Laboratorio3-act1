import socket
import sys
import hashlib
import os
import threading
from datetime import datetime
import time

num_client = int(input('Cuantos clientes desea crear? '))
while (num_client>25 and num_client <= 0):
    num_client = int(input('Por favor ingresar un número válido: '))


class Main:    
    def __init__(self):
        self.lock = threading.Lock()
    def cliente_funct(self, nombre):
        self.lock.acquire()
        
        log = open("./logs/"+nombre+' '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+"log.txt", "w")
        self.lock.release()
        # Crear a TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conectar socket al puerto donde se esta escuchando
        server_address = ('192.168.37.133', 8888)
        print( 'connecting to %s port %s' % server_address)
        sock.connect(server_address)
        file = open("./ArchivosRecibidos/"+nombre+"-prueba-"+str(num_client)+".txt", "w")
       
        
        try:
            
            # Enviar datos
            mensaje = b'Iniciar conexion...'
            print ( 'enviando "%s"' % mensaje)
            sock.sendall(mensaje)
        
            # buscar la respuesta

            confirmacion = sock.recv(32)
            print(confirmacion.decode('utf-8'))
            #hash a comparar
            md5 = hashlib.md5()
            if(confirmacion.decode('utf-8') == "ok"):
                sock.sendall(b'Cual es el nombre del archivo?')
                nA = sock.recv(32)
                nombreArchivo = nA.decode('utf-8') 
                log.write('El nombre es: '+nombreArchivo+'\n')
                
                sock.sendall(b'listo')
                self.lock.acquire()
                hash = sock.recv(32)
                print('Hash enviado por el servidor TCP:',hash.decode('utf-8'))
                sock.sendall(b'Hash recibido')
                self.lock.release()
                
                
                num_paq=0
                start = time.time()

                while (True):
                       
                    data = sock.recv(1024)
                    
                    if data:
                        try:
                            file.write(data.decode('utf-8') + os.linesep)
                            md5.update(data)
                            num_paq+=1
                            
                        except:
                            print('Hubo Error') 
                            sock.sendall(b'Hubo un error al recibir el archivo')
                            break
                        
                    else:
                        print ('Final de lectura del archivo')
                        sock.sendall(b'Archivo recibido')
                        break
                end = time.time()
                
                tam = os.path.getsize("./archivosRecibidos/"+nombre+"-prueba-"+str(num_client)+".txt")
                
                file.close()
                log.write('El nombre del cliente es: '+nombre+'\n')
                log.write('El tamaño del archivo es: '+str(tam/1000000)+' MB'+'\n')
                
               
               
                print("Hash del archivo leido: {0}".format(md5.hexdigest()))
                  
                
                if(hash.decode('utf-8') == md5.hexdigest()):
                    print("Archivo leido")
                    log.write('Entrega del archivo'+'\n')
                else:
                    print("Ocurrio un error al momento de leer el archivo")
                    log.write('Falla de entrega del archivo'+'\n')
                log.write('Tiempo de transferencia: '+str(end-start)+ ' segs'+'\n') 
                log.write('Valor total en bytes recibidos: '+str(tam)+'\n')     
                log.write('Cantidad de paquetes recibidos: '+str(num_paq)+'\n') 
                
                
        finally:
            print ('Cerrar socket')
            sock.close()
            print ('Fin del programa')
            log.close()
            
            

def worker(c, nombre):
        c.cliente_funct(nombre)
        
hilo=Main()
for num_cliente in range(num_client):
    cliente = threading.Thread(name="Cliente%s" %(num_cliente+1),
                               target=worker,
                               args=(hilo,"Cliente%s" %(num_cliente+1))
                              )
    cliente.start()
