from socket import *
import getch


serverPort=0
press=True

def UDPClinet():
    global serverPort
    serverName = ""
    serverPort = 13117
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    clientSocket.bind((serverName,serverPort))
    print("Client started, listening for offer requests...")
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    if((modifiedMessage[0]==254)& (modifiedMessage[1]==237)&(modifiedMessage[2]==190)&(modifiedMessage[3]==239)):
        port=[modifiedMessage[5],modifiedMessage[6]]
        serverPort=int.from_bytes(port,'little')
        print(serverPort)
    print ("Received offer from "+ serverName +",attempting to connect...")
    clientSocket.close()


def TCPClinet():
    serverName = "172.1.0.75"
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    team_name="FCB"
    clientSocket.send(team_name.encode())
    modifiedSentence = clientSocket.recv(1024)
    print (modifiedSentence.decode())
  
    thread_key = threading.Thread(target=_t).start()
    socket_close_thread = threading.Thread(target=_press).start() 

    print("Server disconnected, listening for offer requests...")



def _t():
    while press:
        a= getch.getch()
        clientSocket.send(a.encode())
    
    

def _press():
    while(True):
        if(not clientSocket.connect()):
            press=False
            break


if __name__ == "__main__":
    while(True):
        UDPClinet()
        TCPClinet()
    