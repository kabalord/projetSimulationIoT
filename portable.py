import socket 

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = ('', 5566)

try:
    socket.connect((host, port))
    print("Client connecté !")
    
    data = "Bonjour à toi, je suis le portable ! :)"
    data = data.encode("utf8")
    socket.sendall(data)
        
    reponse = socket.recv(1024)
    print(reponse)
except ConnectionRefusedError:
    print("Connexion au serveur échouée")

finally:
    socket.close()
