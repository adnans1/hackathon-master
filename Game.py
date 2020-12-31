from socket import *
import random


arr=[]
group1=[]
group2=[]
group1_connection_addr=[]
group2_connection_addr=[]
point_group1=0
point_group2=0

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

#recieve and saves the team names in a tuple.
def team_name(connectionSocket,addr): 
    try:
        team_name=connectionSocket.recv(1024)
    except:
        pass
    arr.append((team_name.decode(),connectionSocket,addr))

#starts the game, sends messages to the clients of their names, and notes them to start the game.
def game(connectionSocket,addr):
    global point_group1
    global point_group2
    msg="Welcome to Keyboard Spamming Battle Royale.\n"
    msg=msg+bcolors.OKBLUE + "Group 1:\n==\n"
    for x in group1:
        msg=msg+x+"\n"
    msg=msg+bcolors.FAIL +"Group 2:\n==\n"
    for y in group2:
        msg=msg+y+"\n"
    msg=msg+bcolors.WARNING+"Start pressing keys on your keyboard as fast as you can!!\n"
    try:
        connectionSocket.send(msg.encode())
    except:
        pass
    h=True
    while(h):
        try:
            x=connectionSocket.recv(1024).decode()
        except:
            h=False
            connectionSocket.close()
            arr.clear()
            group1.clear()
            group2.clear()
            group1_connection_addr.clear()
            group2_connection_addr.clear()
            point_group1=0
            point_group2=0
            break
        if (x=="1"):
            if((connectionSocket,addr) in group1_connection_addr):
                point_group1=point_group1+1
            else:
                point_group2=point_group2+1
        else:
            if((connectionSocket,addr) in group1_connection_addr):
                point_group1=point_group1+1
            else:
                point_group2=point_group2+1
    

#Prints the winner(with colors ofcourse :) ).
def print_wins():
    print(bcolors.OKCYAN+"Game over!\nGroup 1 typed in {} characters."+bcolors.FAIL+" Group 2 typed in {} characters.\n".format(point_group1,point_group2)+ bcolors.ENDC)
    if(point_group1>point_group2):
        print(bcolors.OKBLUE+"Group 1 wins!\nCongratulations to the winners:\n=="+bcolors.ENDC)
        for x in group1:
            print(x)

    elif(point_group2>point_group1):
        print(bcolors.FAIL+"Group 2 wins!\nCongratulations to the winners:\n=="+ bcolors.ENDC)
        for x in group2:
            print(x)   
    else:
       print(bcolors.BOLD+"Draw"+ bcolors.ENDC)


#Splits the teams in a random manner.
def randomteam():
    for (i,k,j) in arr:
        x=int(random.random()*10)
        if(x==1):
            group1.append(i)
            group1_connection_addr.append((k,j))
        else:
            group2.append(i)
            group2_connection_addr.append((k,j))