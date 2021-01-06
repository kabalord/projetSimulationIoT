from concurrent.futures import ThreadPoolExecutor
import socket
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

if __name__  == '__main__':
    id = "1"
    counter = 0
    leader = id
    executor = ThreadPoolExecutor(max_workers=5)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = ('', 7777)

    try:
        socket.connect((host, port))    
        logging.info("Client connecté !")

        while True: 
        	if counter == 0:
        		data = id
        		socket.sendall(data.encode("utf8"))
        		counter = 1
        	if counter == 1:
        		msg = socket.recv(1024)
        		print(f"le serveur a répondu :  {msg.decode()}")
        		if msg.decode() < leader:
        			leader = msg.decode()
        		if msg.decode() > leader and leader == id:
        			data = id
        			socket.sendall(data.encode("utf8"))

          
        
  
    except ConnectionRefusedError:
        print("Connexion au serveur échouée")
    
    finally:
        socket.close()