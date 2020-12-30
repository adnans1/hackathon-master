from socket import *
from pynput.keyboard import Listener
import threading


serverPort=0

def UDPClinet():
    global serverPort
    serverName = '192.168.56.1'
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
    serverName = '192.168.56.1'
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    team_name="FCB"
    clientSocket.send(team_name.encode())
    modifiedSentence = clientSocket.recv(1024)
    print (modifiedSentence.decode())

    
    with Listener() as listener:
        listener.on_press = on_press(listener, clientSocket)
        listener.join()

    print("Server disconnected, listening for offer requests...")
    



def on_press(listener, clientSocket):
    def _t():
        while True:
            try:
                clientSocket.recv(1)
            except:
                listener.stop()
                break
    t = threading.Thread(target=_t).start()

    def _press(key):
        print(key)
        clientSocket.send("1".encode())
    return _press


if __name__ == "__main__":
    while(True):
        UDPClinet()
        TCPClinet()
    