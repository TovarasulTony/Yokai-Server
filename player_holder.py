from _thread import *

class PlayerHolder:
    def __init__(self):
        self.player_list = []

    def add_player(self, player, addr, id):
        if len(self.player_list) <= id:
            self.player_list.append(player)
        else:
            self.player_list[id]=player   
        print (addr[0] + " connected")
        start_new_thread(self.clientthread,(player,addr, id))

    def broadcast(self, message, connection):  
        print(len(list_of_clients))
        for clients in list_of_clients:  
            if clients!=connection:  
                try:  
                    clients.send(bytes(message, 'UTF-8'))  
                except:  
                    clients.close()  
  
                    # if the link is broken, we remove the client  
                    print("caca")  
                    self.remove(clients)

    def remove(self, connection):
        if connection in list_of_clients:
            list_of_clients.remove(connection)

    def clientthread(self, conn, addr, id):
        global list_of_clients_info
        info_str = ""
        if len(list_of_clients_info) != 0:
            info_str+=";"
        info_str+=str(id)
        info_str+=","
        info_str+="150"
        info_str+=","
        info_str+="4"
        info_str+=","
        info_str+=str(30+10*id)
        list_of_clients_info.append(info_str)
        print(info_str)
        populate_list_str=""
        for element in list_of_clients_info:
            if populate_list_str != "":
                populate_list_str+=";"
            populate_list_str+=element
            print(element)
        # sends a message to the client whose user object is conn
        conn.send(bytes("id:"+str(id), 'UTF-8'))
        conn.send(bytes("populate_list:"+populate_list_str, 'UTF-8'))
        message_to_send = "populate_list:"+populate_list_str
        print("1111")
        self.broadcast("joined:"+str(id), conn)  
        print("2222")
        self.broadcast(message_to_send, conn)
        print("3333")
  
        while True:  
            try:  
                bytes_message = conn.recv(2048)
                message = bytes_message.decode("utf-8")
                if message[0]=='[':
                    message_bomb_list = message.split('[')
                    message = message_bomb_list[len(message_bomb_list)-1]
                print(message)
                print(77777777777)
                if message:  
                    message_split = message.split(":")
                    if message_split[0] == "moved":
                        print(message)
                        print(88888888888)
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
                    self.broadcast(message_to_send, conn)  
  
                else:  
                    """message may have no content if the connection  
                    is broken, in this case we remove the connection"""
                    print("cucu")  
                    print(message)  
                    self.remove(conn)  
  
            except:  
                continue