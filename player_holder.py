from _thread import *
import json

command = {
  "command_type": "INVALID",
  "message": "",
  "values": ""
}

command = {
  "command_type": "INVALID",
  "message": "",
  "values": ""
}

player_info = {
  "id": -1,
  "connection": None,
  "address": ""
}

player_position = {
  "id": None,
  "x": None,
  "y": None,
  "z": None
}

class PlayerHolder:
    def __init__(self):
        self.player_list = []
        self.player_info_list = {}
        self.current_id_count = 0

    def add_player(self, conn, addr):
        print("HOLDER")
        self.current_id_count += 1
        added_player = player_info
        added_player["id"] = self.current_id_count
        added_player["connection"] = conn
        added_player["address"] = addr
        self.player_info_list[added_player["id"]] = added_player
        print (addr[0] + " connected")
        player_command = command
        player_command["command_type"] = "GAME"
        player_command["message"] = "set_id"
        player_command["values"] = added_player["id"]
        added_player["connection"].send(bytes(json.dumps(player_command), 'UTF-8'))

        position_command = player_position
        position_command["x"] = added_player["id"]
        position_command["x"] = 150
        position_command["y"] = 4
        position_command["z"] = 30+10*added_player["id"]


        player_command = command
        player_command["command_type"] = "GAME"
        player_command["message"] = "set_position"
        player_command["values"] = position_command
        added_player["connection"].send(bytes(json.dumps(player_command), 'UTF-8'))

        start_new_thread(self.clientthread,(player,addr, id))

    def broadcast(self, message, connection):  
        print(len(self.player_list))
        for clients in self.player_list:  
            if clients!=connection:  
                try:  
                    clients.send(bytes(message, 'UTF-8'))  
                except:  
                    clients.close()  

                    # if the link is broken, we remove the client  
                    print("caca")  
                    self.remove(clients)

    def remove(self, connection):
        if connection in self.player_list:
            self.player_list.remove(connection)

    def setup_player(self, conn):

        info_str = ""
        if len(self.player_info_list) != 0:
            info_str+=";"
        info_str+=str(id)
        info_str+=","
        info_str+="150"
        info_str+=","
        info_str+="4"
        info_str+=","
        info_str+=str(30+10*id)
        self.player_info_list.append(info_str)
        print(info_str)
        populate_list_str=""
        for element in self.player_info_list:
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

    def clientthread(self, conn, addr="placeholder"):
        #self.setup_player(conn)
        info_str = ""
        if len(self.player_info_list) != 0:
            info_str+=";"
        info_str+=str(id)
        info_str+=","
        info_str+="150"
        info_str+=","
        info_str+="4"
        info_str+=","
        info_str+=str(30+10*id)
        self.player_info_list.append(info_str)
        print(info_str)
        populate_list_str=""
        for element in self.player_info_list:
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
                        self.player_info_list[int(player_info[0])-1] = info_str
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