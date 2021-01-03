import sys
import zmq
import time
from zmq import EAGAIN

def clearSocketBuffer(pull_socket):
    print("je nettoie mon pull socket buffer \n")
    time.sleep(1)  
    while(True):
        try: 
            recieved_message = pull_socket.recv_string()
            print("je nettoie %s message est envoyé par %s \n"%(recieved_message.split(" ")[0],recieved_message.split(" ")[1]))
        except  zmq.error.Again as e:
            print("************************************************ \n")
            return

def leaderCheckElection(dec,push_socket,pull_socket,my_ip_port):
    try:
        recieved_message = pull_socket.recv_string()
        print("au moment : %i \n"%(time.time()-1585656000))
        if(recieved_message.split(" ")[0] == "Election"):
            if (dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                push_socket.connect("tcp://%s"%recieved_message.split(" ")[1])
                push_socket.send_string("%s %s" %("Leader",my_ip_port))
                push_socket.disconnect("tcp://%s"%recieved_message.split(" ")[1])
                print("J'ai envoyé un message de leader à %s \n"%recieved_message.split(" ")[1])
                print("************************************************ \n")
                print("au moment : %i \n"%(time.time()-1585656000))
                print("%s je suis le leader et je fais la tâche \n"%my_ip_port)
            
        elif(recieved_message.split(" ")[0] == "Leader"):
            print("je reçu un message du leader à partir de %s \n"%recieved_message.split(" ")[1])
            if(dec[my_ip_port] < dec[recieved_message.split(" ")[1]]):
                print("sa priority plus haut \n")
                print("************************************************ \n")
                return recieved_message.split(" ")[1]   
             
    except zmq.error.Again as e:
        return 0    
    return 1        

def machineCheckElection(dec,task_socket,push_socket,pull_socket,my_ip_port,leader_ip_port):
    try: 
        recieved_message = pull_socket.recv_string()
        print("au moment : %i \n"%(time.time()-1585656000))
        if(recieved_message.split(" ")[0] == "Election"):
            print("je reçu un message d'éléction à partir de %s \n"%recieved_message.split(" ")[1])
            try:
                task_socket.send_string("le leader est vivant")
                task_socket.recv_string()
            except zmq.error.Again as e:
                if(dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                    push_socket.connect("tcp://%s"%recieved_message.split(" ")[1])
                    push_socket.send_string("%s %s" % ("Ok",my_ip_port)) 
                    push_socket.disconnect("tcp://%s"%recieved_message.split(" ")[1])
                    print("au moment : %i \n"%(time.time()-1585656000))
                    print("j'envoie message OK à %s \n" %(recieved_message.split(" ")[1]))
                    print("************************************************ \n")
                    
                    return electLeader(dec,push_socket,pull_socket,my_ip_port,okay_time)
                else:
                    print("j'attends lorsque le leader m'envoie un message")
                    while(True):
                        try: 
                            recieved_message = pull_socket.recv_string()
                            if(recieved_message.split(" ")[0] == "Leader"):
                                print("au moment : %i \n"%(time.time()-1585656000))
                                print("je reçu un message du leader à partir de %s \n"%recieved_message.split(" ")[1])
                                print("************************************************ \n")
                                
                                return recieved_message.split(" ")[1] 
                        except  zmq.error.Again as e:
                            dummy = 1 
            print("le leader est encore vivant \n")
            print("************************************************ \n")
            print("au moment : %i \n"%(time.time()-1585656000))
            print("%s je suis une non leader machine et je fais ma tâche \n"%my_ip_port)
        elif(recieved_message.split(" ")[0] == "Leader"):
            print("je reçu un message du leader  à partir de %s \n"%recieved_message.split(" ")[1])
            if(dec[leader_ip_port] < dec[recieved_message.split(" ")[1]]):
                print("sa priority plus haut que cela du leader  \n")
                print("************************************************ \n")
                
                return recieved_message.split(" ")[1] 
    except  zmq.error.Again as e:
        dummy = 1
    return 0    

def checkPullSocket(dec,push_socket,pull_socket,my_ip_port):
    try: 
        recieved_message = pull_socket.recv_string()
        print("sa priority plus haut : %i \n"%(time.time()-1585656000))
        if(recieved_message.split(" ")[0] == "Election"):
            print("je reçu un message d'éléction à partir de %s \n"%recieved_message.split(" ")[1])
            if(dec[my_ip_port] > dec[recieved_message.split(" ")[1]]):
                push_socket.connect("tcp://%s"%recieved_message.split(" ")[1])
                push_socket.send_string("%s %s" % ("Ok",my_ip_port)) 
                push_socket.disconnect("tcp://%s"%recieved_message.split(" ")[1])
                print("au moment : %i \n"%(time.time()-1585656000))
                print("message Ok envoyé à %s \n" %(recieved_message.split(" ")[1]))
        elif(recieved_message.split(" ")[0] == "Ok"):
            print("j'ai reçu un message OK à partir de %s \n"%recieved_message.split(" ")[1])
            return 1     
        elif(recieved_message.split(" ")[0] == "Leader"):
            print("j'ai reçu un message du leader à partir de %s \n"%recieved_message.split(" ")[1])
            print("************************************************ \n")
            return recieved_message.split(" ")[1]   
    except  zmq.error.Again as e:
        return 0        
    return 0            

def electLeader(dec,push_socket,pull_socket,my_ip_port, okay_time):  
    
    recieved_ok = False
    i = 0
    for k,v in dec.items():         
        if(v > dec[my_ip_port]):
            push_socket.connect("tcp://%s"%k)
            push_socket.send_string("%s %s" %("Election",my_ip_port))
            push_socket.disconnect("tcp://%s"%k)
            print("au moment : %i \n"%(time.time()-1585656000))
            print("j'envoie le message à %s \n"%k)

            
            out = checkPullSocket(dec,push_socket,pull_socket,my_ip_port)
            if(out == 1):   
                recieved_ok = True
                break
            elif(out != 0):  
                return out
        i+=1
    
    
    milliseconds = int(round(time.time() * 1000))
    counter = 0    
    while(not recieved_ok and counter < okay_time): 
        out = checkPullSocket(dec,push_socket,pull_socket,my_ip_port)
        if(out == 1):   
            recieved_ok = True
            break
        elif(out != 0):  
            return out

        milliseconds2 = int(round(time.time() * 1000))
        counter +=  milliseconds2 - milliseconds
        milliseconds = milliseconds2   
    print("************************************************ \n")
    
    
    leader = ""
    if (recieved_ok == False):
        for k,v in dec.items():
            if(k != my_ip_port):
                push_socket.connect("tcp://%s"%k)
                push_socket.send_string("%s %s" %("Leader",my_ip_port))
                push_socket.disconnect("tcp://%s"%k)
                print("au moment : %i \n"%(time.time()-1585656000))
                print("j'envoie un message du leader à %s \n"%k)
        print("************************************************ \n")
        return my_ip_port  
    
    else:
        while(True):
            try: 
                recieved_message = pull_socket.recv_string()
                if(recieved_message.split(" ")[0] == "Leader"):
                    print("au moment : %i \n"%(time.time()-1585656000))
                    print("j'ai reçu un message du leader à partir de \n"%recieved_message.split(" ")[1])
                    print("************************************************ \n")
                    return recieved_message.split(" ")[1] 
            except  zmq.error.Again as e:
                dummy = 1     