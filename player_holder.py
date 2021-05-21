from _thread import *
import copy
import json
from clues import CluesHandler

command_dict = {
  "command_type": "INVALID",
  "message": "",
  "values": ""
}

player_position_json = {
  "id": None,
  "x": None,
  "y": None,
  "z": None,
  "y_rotation": None,
}

player_struct_dict = {
  "connection": None,
  "address": "",
  "player_info": copy.deepcopy(player_position_json)
}

class PlayerHolder:
    def __init__(self, lobby_ref):
        self.player_dict = {}
        self.lobby_ref = lobby_ref
        self.id_count = -1
        self.clue_handler = CluesHandler()
        #self.terminate_thread_flag = False

    def add_player(self, player):
        self.id_count+=1
        added_player = copy.deepcopy(player_struct_dict)
        added_player["player_info"] = self.setup_player(player)
        added_player["connection"] = player["connection"]
        added_player["address"] = player["address"]
        self.make_client_command(added_player, "set_phantom_type", self.clue_handler.get_phantom_type())
        self.player_dict[added_player["player_info"]["id"]] = added_player
        self.inform_lobby_players_number()
        self.make_client_command(added_player, "set_primordial_id", added_player["player_info"]["id"])
        self.send_init_info(added_player)
        self.make_client_command(added_player, "set_clues_spawn", json.dumps(self.clue_handler.get_clues_holder()))
        self.broadcast_command(added_player, "add_new_player", json.dumps(added_player["player_info"]))
        print("player added: " + str(added_player["player_info"]["id"]))
        start_new_thread(self.clientthread, (added_player,))

    def setup_player(self, player):
        added_player_position = copy.deepcopy(player_position_json)
        added_player_position["id"] = self.id_count
        added_player_position["x"] = 150
        added_player_position["y"] = 4
        added_player_position["z"] = 30 + 10 * added_player_position["id"]
        added_player_position["y_rotation"] = 0
        return added_player_position

    def send_init_info(self, _player):
        players_info_list = []
        for player_id in self.player_dict:
            player = self.player_dict[player_id]
            if player == None:
                continue
            if player["player_info"]["id"] == None:
                continue
            players_info_list.append(player["player_info"])
        self.make_client_command(player, "set_primary_position", json.dumps(players_info_list))

    def remove(self, player):
        if player["player_info"]["id"] in self.player_dict:
            self.player_dict.pop(player["player_info"]["id"])
        self.broadcast_command(player, "remove_player", player["player_info"]["id"])
        self.inform_lobby_players_number()

    def clientthread(self, player):
        terminate_thread_flag = False
        while True:
            try:
                if terminate_thread_flag == True:
                    print("Lobby Thread terminated for address: " + player["address"])
                    return
                bytes_message = player["connection"].recv(2048)
                message_bulk = bytes_message.decode("utf-8")
                #print(message_bulk)
                message_list = message_bulk.split('$')
                for message in message_list:
                    if message == "-" or message == "--":
                        continue
                    if message == "":
                        print("Broken connection")
                        self.remove(player)
                        return
                        """message may have no content if the connection  
                        is broken, in this case we remove the connection"""
                        continue
                    message = json.loads(message)
                    terminate_thread_flag = self.execute_command(player, message)
            except:  
                continue

    def execute_command(self, player, received_command):
        print(received_command["message"])
        if received_command["message"] == "test_command":
            print(2222)
            print(received_command["values"])
            self.broadcast_command(player, "test_command", received_command["values"])
            return False
        if received_command["message"] == "break_connection":
            print("break_connection")
            self.remove(player)
            print("player removed: " + str(player["player_info"]["id"]))
            return True
        if received_command["message"] == "player_moved":
            player_new_position = json.loads(received_command["values"])
            self.player_dict[player_new_position["id"]]["player_info"]=player_new_position
            self.broadcast_command(player, "update_player_position", json.dumps(player_new_position))
            return False
        if received_command["message"] == "destroy_object":
            self.broadcast_command(player, "destroy_object", received_command["values"])
            return False
        if received_command["message"] == "toggle_flashlight":
            self.broadcast_command(player, "toggle_flashlight", received_command["values"])
            return False
        return False

    def send_message_to_player(self, player, message_json):
        string_message = "$"
        string_message += json.dumps(message_json)
        string_message += "$"
        player["connection"].sendall(bytes(string_message, 'UTF-8'))

    def make_client_command(self, player, message, values=""):
        command_json = copy.deepcopy(command_dict)
        command_json["command_type"] = "LEVEL"
        command_json["message"] = message
        command_json["values"] = values
        self.send_message_to_player(player, command_json)

    def broadcast_command(self, player, message, values=""):
        for player_id in self.player_dict:
            player_in_list = self.player_dict[player_id]
            if player_in_list["player_info"]["id"] == player["player_info"]["id"]:
                continue
            #print("brodcast to: " + str(player_in_list["player_info"]["id"]))
            self.make_client_command(player_in_list, message, values)

    def inform_lobby_players_number(self):
        self.lobby_ref.number_of_players_changed(len(self.player_dict)) 