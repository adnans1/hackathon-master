from socket import *
import time
import threading
import Game
import scapy.all as Scapy

clientsoket=[]

#Colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#we get the server ip through this function.
def get_ip(interface):
    return Scapy.get_if_addr(interface)

#UDP Server Side
#This function starts the udp server, the udp server and disconnect after 10 seconeds.
def UDPServer(interface=Scapy.conf.iface):
    serverport=13117
    serverSocket= socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
    serverSocket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    TCPPort=TCPServer(interface)
    message_bytes=[]
    message_bytes.extend(bytes.fromhex("feedbeef"))
    message_bytes.extend([2])
    message_bytes.extend(TCPPort.to_bytes(2,'little'))
    print("Server started, listening on IP address " + gethostbyname(gethostname()))
    for i in range(10):
        try:
            serverSocket.sendto(bytes(message_bytes), ('<broadcast>', serverport))
            time.sleep(1)
        except:
            break
    
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


#TCP Server Side.    
#This function starts the TCP server and run the game and calls the game
#function in the Game module to calculate the result and disconnect after 10 seconds.
def TCPServer(interface) :
    serverPort = 0
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.settimeout(10)
    serverSocket.bind((get_ip(interface),serverPort))
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
                Clinethread = threading.Thread(target = Game.team_name, args=(connectionSocket,addr)).start()
                client_arr.append(Clinethread)
            except:
                flag=False
    TCPThread = threading.Thread(target = _accpet_thread)
    TCPThread.start()
    return TCPPort
        


if __name__=='__main__':
    while(1):
        UDPServer(Scapy.conf.iface)