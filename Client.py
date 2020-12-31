from socket import *
#from pynput.keyboard import Listener
import time
import msvcrt
import threading

serverPorttcp=0

def UDPClinet():
    serverName = '192.168.1.15'
    serverPort = 13117
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    clientSocket.bind((serverName,serverPort))
    print("Client started, listening for offer requests...")
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    if((modifiedMessage[0]==254)& (modifiedMessage[1]==237)&(modifiedMessage[2]==190)&(modifiedMessage[3]==239)):	
        port=[modifiedMessage[5],modifiedMessage[6]]
        serverPorttcp=int.from_bytes(port,'little')
    print ("Received offer from "+ serverName +",attempting to connect...")
    clientSocket.close()


def TCPClinet():
    serverName = '192.168.1.15'
    serverPorttcp = 2020
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPorttcp))
    team_name="FCB"
    clientSocket.send(team_name.encode())
    modifiedSentence = clientSocket.recv(1024)
    print (modifiedSentence.decode())
#cahnfge
    end=time.time()+10
    flag = True
    clientSocket.settimeout(10)
    while ((time.time() < end) & flag) :        
        if msvcrt.kbhit():
            char= msvcrt.getch()
            pKey=char.decode('ASCII')
            print(pKey.encode())
            try:
                clientSocket.send(pKey.encode())
            except:
                flag = False

    print("Server disconnected, listening for offer requests...")
    



if __name__=='__main__':
    while(True):
        UDPClinet()
        TCPClinet()