from _thread import *
import copy
import json

command_dict = {
  "command_type": "INVALID",
  "message": "",
  "values": ""
}

player_dict = {
  "id": -1,
  "connection": None,
  "address": ""
}

class Lobby:
    def __init__(self, command_callback):
        self.lobby_list = []
        self.command_callback = command_callback
        self.id_count = -1
        self.game_players_count = 0

    def add_potential_player(self, conn, addr):
        self.id_count+=1
        new_player = copy.deepcopy(player_dict)
        new_player["id"] = self.id_count
        new_player["connection"] = conn
        new_player["address"] = addr
        self.lobby_list.append(new_player) 
        self.setup_lobby_player(new_player) 
        start_new_thread(self.clientthread, (new_player,))

    def remove_potential_player(self, player):
        self.lobby_list.remove(player)
        self.broadcast_command(player, "lobby_count", len(self.lobby_list))

    def setup_lobby_player(self, player):
        self.make_client_command(player, "game_count", self.game_players_count)
        self.broadcast_command(player, "lobby_count", len(self.lobby_list))

    def send_message_to_player(self, player, message_json):
        string_message = "$"
        string_message += json.dumps(message_json)
        string_message += "$"
        player["connection"].send(bytes(json.dumps(message_json), 'UTF-8'))

    def clientthread(self, player):
        terminate_thread_flag = False
        while True:  
            try:
                bytes_message = player["connection"].recv(2048)
                message_bulk = bytes_message.decode("utf-8")
                message_list = message_bulk.split('$')
                for message in message_list:
                    if message == "":
                        """message may have no content if the connection  
                        is broken, in this case we remove the connection"""
                        continue
                    message = json.loads(message)
                    terminate_thread_flag = self.execute_command(player, message)
                    print(terminate_thread_flag)
                    if terminate_thread_flag == True:
                        print("Lobby Thread terminated for address: " + player["address"])
                        return
            except:
                if terminate_thread_flag == True:
                    return
                continue

    def execute_command(self, player, message):
        if message["message"] == "enter_game":
            self.command_callback(player, message)
            return True
        return False

    def make_client_command(self, player, message, values=""):
        command_json = copy.deepcopy(command_dict)
        command_json["command_type"] = "LOBBY"
        command_json["message"] = message
        command_json["values"] = values
        self.send_message_to_player(player, command_json)

    def broadcast_command(self, player, message, values=""):
        for player_in_list in self.lobby_list:
            self.make_client_command(player_in_list, message, values)

    def number_of_players_changed(self, new_number):
        self.game_players_count = new_number
        self.broadcast_command(player, "game_count", self.game_players_count)