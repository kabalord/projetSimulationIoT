from concurrent.futures import ThreadPoolExecutor
import socket
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
#connection
host, port = ('', 5566)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host, port))
socket.listen(5)

def run():
    data = f"The time is {time.time()}"
    data = data.encode("utf8")
    conn.sendall(data)
    data = conn.recv(1024)
    data = data.decode("utf8")
    print(data)

if __name__ == '__main__':
     executor = ThreadPoolExecutor(max_workers=5)
     logging.info("le serveur est démarré !")
     
#threading
while True:    
    conn, address = socket.accept()
    print(f"Un client vient de se connecter depuis {address}")
    
    executor.submit(run)

conn.close()
socket.close()
        

