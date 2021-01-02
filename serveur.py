import socket
import time 
import threading

#threading
class ThreadForClient(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        
    def run(self):
        data = f"The time is {time.time()}"
        data = data.encode("utf8")
        conn.sendall(data)
        data = conn.recv(1024)
        data = data.decode("utf8")
        print(data)
        

#connection
host, port = ('', 5566)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host, port))
socket.listen(5)
print("le serveur est démarré !")

while True:	
    conn, address = socket.accept()
    print(f"Un client vient de se connecter depuis {address}")
    
    my_thread = ThreadForClient(conn)
    my_thread.start()

conn.close()
socket.close()
