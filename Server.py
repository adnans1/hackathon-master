from socket import *
import time
import threading
import Game
import scapy.all as Scapy

clientsoket=[]
TCPPort=0
client_arr=[]

def get_ip(interface):
    return Scapy.get_if_addr(interface)


def UDPServer(interface=Scapy.conf.iface):
    serverport=13117
    serverSocket= socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
    serverSocket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    TCPServer(interface)
    message_bytes=[]
    message_bytes.extend(bytes.fromhex("feedbeef"))
    message_bytes.extend([2])
    message_bytes.extend(TCPPort.to_bytes(2,'little'))
    print("Server started, listening on IP address " + get_ip(interface))
    for i in range(10):
        serverSocket.sendto(bytes(message_bytes), ('<broadcast>', serverport))
        time.sleep(1)
        print ("hi hi hi")
    
    Game.randomteam()
    for (x,y) in clientsoket :
        gamethread=threading.Thread(target = Game.game,args=(x,y)).start()
    time.sleep(10)
    Game.print_wins()
    serverSocket.close()  
    for (x,y) in clientsoket :     
        x.close()

    print("Server disconnected, listening for offer requests...")
    
        
def TCPServer(interface) :
    global client_arr
    global clientsoket
    global TCPPort
    serverPort = 0
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.settimeout(10)
    serverSocket.bind( (get_ip(interface),serverPort) )
    TCPPort=serverSocket.getsockname()[1]
    serverSocket.listen(1)

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
                flag = False
    TCPThread = threading.Thread(target = _accpet_thread)
    TCPThread.start()
            


if __name__ == "__main__":
    while(1):
        UDPServer('eth1')