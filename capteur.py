from concurrent.futures import ThreadPoolExecutor
import socket
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

if __name__ == '__main__':
    
    executor = ThreadPoolExecutor(max_workers=5)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = ('', 7777)
    
    try:
        socket.connect((host, port))    
        logging.info("Client connecté !")
        
        time.sleep(1)
        data = f"The time is {time.time()}"
        data = data.encode("utf8")
        
        data = input("envoyer un message : ")
        data = data.encode("utf8")
        socket.sendall(data)
        
            
        data = socket.recv(1024)
        print(f"serveur a répondu : {data.decode()}")
    
    except ConnectionRefusedError:
        print("Connexion au serveur échouée")
    
    finally:
        socket.close()