from socket import *
import time
import threading
import Game

clientsoket=[]
TCPPort=0

def UDPServer():
    serverport=13117
    serverSocket= socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
    serverSocket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    TCPServer()
    message_bytes=[]
    message_bytes.extend(bytes.fromhex("feedbeef"))
    message_bytes.extend([2])
    message_bytes.extend(TCPPort.to_bytes(2,'little'))

    print("Server started, listening on IP address " + gethostbyname(gethostname()))
    for i in range(10):
        serverSocket.sendto(bytes(message_bytes), ('<broadcast>', serverport))
        time.sleep(1)
    
    Game.randomteam()
    for (x,y) in clientsoket :
        gamethread=threading.Thread(target = Game.game,args=(x,y)).start()
    time.sleep(10)
    Game.print_wins()
    serverSocket.close()
    for (a,b) in clientsoket:
        a.close()
    clientsoket.clear()
    print("Server disconnected, listening for offer requests...")

            
        
def TCPServer() :
    serverPort = 2020
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.settimeout(10)
    serverSocket.bind(('192.168.1.15',serverPort))
    TCPPort=serverSocket.getsockname()[1]
    serverSocket.listen(1)
    client_arr=[]
    team_arr=[]
    def _accpet_thread():
        flag=True
        while (flag):
            try:
                connectionSocket, addr = serverSocket.accept()
                clientsoket.append((connectionSocket, addr))
                #creat a thread 
                Clinethread = threading.Thread(target = Game.team_name, args=(connectionSocket,addr)).start()
                client_arr.append(Clinethread)
            except:
                flag=False
    TCPThread = threading.Thread(target = _accpet_thread)
    TCPThread.start()
        


if __name__=='__main__':
    while(1):
        UDPServer()