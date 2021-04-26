from _thread import *
import copy
import json

command_dict = {
  "command_type": "INVALID",
  "message": "",
  "values": ""
}

player_position_dict = {
  "x": None,
  "y": None,
  "z": None
}

player_info_dict = {
  "id": -1,
  "connection": None,
  "address": "",
  "player_position": copy.deepcopy(player_position_dict)
}

class PlayerHolder:
    def __init__(self):
        self.player_list = []
        #self.player_info_list = {}

    def add_player(self, player):
        added_player = copy.deepcopy(player_info_dict)
        added_player["id"] = player["id"]
        added_player["connection"] = player["connection"]
        added_player["address"] = player["address"]
        print(765736737)
        print(player["id"])
        print(added_player["id"])
        added_player["id"] =7000
        print(player["id"])
        print(765736737)
        self.player_list.insert(added_player["id"], added_player)
        self.send_primordial_id(added_player)
        self.set_player_primary_position(added_player)
        self.send_init_info(added_player)
        #-----------ok code line#-----------
        self.player_list.append(added_player)  
        start_new_thread(self.clientthread, (new_player,))

    def set_player_primary_position(self, player):
        added_player_position = copy.deepcopy(player_position_dict)
        added_player_position["x"] = 150
        added_player_position["y"] = 4
        added_player_position["z"] = 30 + 10 * player["id"]
        player["player_position"] = added_player_position

    def send_primordial_id(self, player):
        player_id_json = copy.deepcopy(command_dict)
        player_id_json["command_type"] = "LEVEL"
        player_id_json["message"] = "set_primordial_id"
        player_id_json["values"] = player["id"]
        self.send_message_to_player(player, player_id_json)

    def send_init_info(self, player):
        players_info_list = []
        for player_info in self.player_list:
            if player_info == None or player_info["id"] == None:
                continue
            player_info_json = {
              "id": player_info["id"],
              "x": player_info["player_position"]["x"],
              "y": player_info["player_position"]["y"],
              "z": player_info["player_position"]["z"]
            }
            players_info_list.append(player_info_json)
        player_json = copy.deepcopy(command_dict)
        player_json["command_type"] = "LEVEL"
        player_json["message"] = "set_primary_position"
        player_json["values"] = json.dumps(players_info_list)
        self.send_message_to_player(player, player_json)

    def remove(self, connection):
        if connection in self.player_list:
            self.player_list.remove(connection)

    def clientthread(self, player):
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

    def send_message_to_player(self, player, message_json):
        print(player["connection"])
        print(player["connection"].send(bytes(json.dumps(message_json), 'UTF-8')))