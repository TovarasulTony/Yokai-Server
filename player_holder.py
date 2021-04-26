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
        self.player_list.insert(added_player["id"], added_player)
        self.send_primordial_id(added_player)
        self.set_player_primary_position(added_player)
        self.send_init_info(added_player)
        start_new_thread(self.clientthread, (added_player,))

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
        terminate_thread_flag = False
        while True:
            try:
                if terminate_thread_flag == True:
                    print("Lobby Thread terminated for address: " + player["address"])
                    return
                bytes_message = player["connection"].recv(2048)
                message_bulk = bytes_message.decode("utf-8")
                message_list = message_bulk.split('$')
                for message in message_list:
                    #print(88888)
                    #print(message)
                    if message == "":
                        """message may have no content if the connection  
                        is broken, in this case we remove the connection"""
                        #print("cucu")  
                        #print("MESAJ GOL")
                        #player["connection"].close()
                        #self.remove_potential_player(player["connection"])
                        #self.remove(player["connection"])  
                        continue
                    message = json.loads(message)
                    terminate_thread_flag = self.execute_command(player, message)
            except:  
                continue

    def execute_command(self, player, message):
        print(666677777)
        if message["message"] == "player_moved":
            print(55555555555)
            #print(message["values"])
            print(message["values"])
            print(type(message["values"]))
            player_new_position = json.loads(message["values"])
            print(player_new_position)
            print(player_new_position['x'])
            print(type(player_new_position['x']))
            #player_list[player_new_position['id']]
            return False
        return False

    def send_message_to_player(self, player, message_json):
        print(player["connection"])
        print(player["connection"].send(bytes(json.dumps(message_json), 'UTF-8')))