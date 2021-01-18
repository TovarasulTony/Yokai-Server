# Python program to implement server side of chat room.  
import socket  
import select  
import sys  
from _thread import *
  
"""The first argument AF_INET is the address domain of the  
socket. This is used when we have an Internet Domain with  
any two hosts The second argument is the type of socket.  
SOCK_STREAM means that data or characters are read in  
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
  

# takes the first argument from command prompt as IP address  
IP_address = "23.95.226.141" 
  
# takes second argument from command prompt as port number  
Port = 65432
  
"""  
binds the server to an entered IP address and at the  
specified port number.  
The client must be aware of these parameters  
"""
server.bind((IP_address, Port))  
  
"""  
listens for 100 active connections. This number can be  
increased as per convenience.  
"""
server.listen(2)  
  
list_of_clients = []  
list_of_clients_info = []
  
def clientthread(conn, addr, id):
    info_str = ""
    if len(list_of_clients_info) != 0:
        info_str+=";"
    info_str+=str(id)
    info_str+=","
    info_str+=str(10*id)
    info_str+=","
    info_str+="0"
    info_str+=","
    info_str+="0"
    list_of_clients_info.append(info_str)
    populate_list_str=""
    for element in list_of_clients_info:
        if populate_list_str != "":
            populate_list_str+=";"
        populate_list_str+=element
    # sends a message to the client whose user object is conn
    conn.send(bytes("id:"+str(id), 'UTF-8'))
    conn.send(bytes("populate_list:"+populate_list_str, 'UTF-8'))
    message_to_send = "populate_list:"+populate_list_str
    broadcast(message_to_send, conn)
  
    while True:  
            try:  
                message = conn.recv(2048)  
                if message:  
                    message_split = message.split(":")
                    if message_split[0] == "moved":
                        player_info = message_split[1].split(",")
                        info_str=""
                        info_str+=player_info[0]
                        info_str+=","
                        info_str+=player_info[1]
                        info_str+=","
                        info_str+=player_info[2]
                        info_str+=","
                        info_str+=player_info[3]
                        list_of_clients_info[int(player_info[0])-1] = info_str
                    """prints the message and address of the  
                    user who just sent the message on the server  
                    terminal"""
                    print ("<" + addr[0] + "> " + message)  
  
                    # Calls broadcast function to send message to all  
                    message_to_send = message  
                    broadcast(message_to_send, conn)  
  
                else:  
                    """message may have no content if the connection  
                    is broken, in this case we remove the connection"""
                    print("cucu")  
                    print(message)  
                    remove(conn)  
  
            except:  
                continue
  
"""Using the below function, we broadcast the message to all  
clients who's object is not the same as the one sending  
the message """
def broadcast(message, connection):  
    for clients in list_of_clients:  
        if clients!=connection:  
            try:  
                clients.send(message)  
            except:  
                clients.close()  
  
                # if the link is broken, we remove the client  
                print("caca")  
                remove(clients)  
  
"""The following function simply removes the object  
from the list that was created at the beginning of  
the program"""
def remove(connection):
    if connection in list_of_clients:  
        list_of_clients.remove(connection)  

id = 0
while True:  
    #global id 
    """Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address of the client that just  
    connected"""
    conn, addr = server.accept()  
  
    """Maintains a list of clients for ease of broadcasting  
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)  
  
    # prints the address of the user that just connected  
    print (addr[0] + " connected") 
  
    # creates and individual thread for every user  
    # that connects
    id+=1
    broadcast("joined:"+str(id), conn)  
    start_new_thread(clientthread,(conn,addr, id))    
  
conn.close()  
server.close()  