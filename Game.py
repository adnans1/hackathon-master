from socket import *
import random



arr=[]
group1=[]
group2=[]
group1_connection_addr=[]
group2_connection_addr=[]
point_group1=0
point_group2=0


def team_name(connectionSocket,addr): 
    team_name=connectionSocket.recv(1024)
    arr.append((team_name.decode(),connectionSocket,addr))


def game(connectionSocket,addr):
    global point_group1
    global point_group2
    msg="Welcome to Keyboard Spamming Battle Royale.\n"
    msg=msg+"Group 1:\n==\n"
    for x in group1:
        msg=msg+x+"\n"
    msg=msg+"Group 2:\n==\n"
    for y in group2:
        msg=msg+y+"\n"
    msg=msg+"Start pressing keys on your keyboard as fast as you can!!\n"
    connectionSocket.send(msg.encode())
    h=True
    while(h):
        try:
            x=connectionSocket.recv(1024).decode()
        except:
            h=False
            connectionSocket.close()
            break
        if (x=="1"):
            if((connectionSocket,addr) in group1_connection_addr):
                point_group1=point_group1+1
                print("one point")
            else:
                point_group2=point_group2+1
                print("one point from anthor")
        else:
            if((connectionSocket,addr) in group1_connection_addr):
                point_group1=point_group1+1
            else:
                point_group2=point_group2+1
    

def print_wins():
    print("Game over!\nGroup 1 typed in {} characters. Group 2 typed in {} characters.\n".format(point_group1,point_group2))
    if(point_group1>point_group2):
        print("Group 1 wins!\nCongratulations to the winners:\n==")
        for x in group1:
            print(x)

    elif(point_group2>point_group1):
        print("Group 2 wins!\nCongratulations to the winners:\n==")
        for x in group2:
            print(x)   
    else:
       print("Drow")  


def randomteam():
    for (i,k,j) in arr:
        x=int(random.random()*10)
        if(x==1):
            group1.append(i)
            group1_connection_addr.append((k,j))
        else:
            group2.append(i)
            group2_connection_addr.append((k,j))


  


