from _thread import *
import copy
import json
from library import info_dict

command_dict = {
  "command_type": "INVALID",
  "message": "",
  "values": ""
}

player_dict = {
  "connection": None,
  "address": ""
}

class Lobby:
    def __init__(self, command_callback):
        self.lobby_list = []
        self.command_callback = command_callback
        self.game_players_count = 0

    def add_potential_player(self, conn, addr):
        new_player = copy.deepcopy(player_dict)
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
        self.make_client_command(player, "server_version", info_dict["server_version"])
        self.broadcast_command(player, "lobby_count", len(self.lobby_list))

    def clientthread(self, player):
        terminate_thread_flag = False
        last_message = ""
        while True:  
            try:
                if terminate_thread_flag == True:
                    print("Lobby Thread terminated for address: " + str(player["address"]))
                    return
                bytes_message = player["connection"].recv(1024)
                message_bulk = last_message
                message_bulk += bytes_message.decode("utf-8")
                print(message_bulk)
                message_list = message_bulk.split('$')
                if message_list[len(message_list) - 1] != "-" or message_list[len(message_list) - 1] != "--":
                    last_message = message_list[len(message_list) - 1]
                    message_list = message_list[:-1]
                else:
                    last_message = ""
                for message in message_list:
                    if message == "-" or message == "--":
                        continue
                    if message == "":
                        print("Broken connection")
                        self.remove_potential_player(player)
                        terminate_thread_flag = True
                    message = json.loads(message)
                    terminate_thread_flag = self.execute_command(player, message)
            except: 
                print("Exceptie in holder")
                print("Lobby Thread terminated for address: " + str(player["address"]))
                return

    def execute_command(self, player, message):
        print("$$$$$$")
        print(message["message"])
        if message["message"] == "enter_game":
            self.command_callback(player, message)
            return True
        if message["message"] == "break_connection":
            print("break_connection")
            self.remove_potential_player(player)
            return True
        return False

    def send_message_to_player(self, player, message_json):
        string_message = "$"
        string_message += json.dumps(message_json)
        string_message += "$"
        player["connection"].sendall(bytes(string_message, 'UTF-8'))

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
        self.broadcast_command(None, "game_count", self.game_players_count)