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

    def add_potential_player(self, conn, addr):
        self.id_count+=1
        new_player = copy.deepcopy(player_dict)
        new_player["id"] = self.id_count
        new_player["connection"] = conn
        new_player["address"] = addr
        self.lobby_list.append(new_player) 
        self.setup_lobby_player(new_player) 
        print(str(new_player["address"]) + " connected")
        start_new_thread(self.clientthread, (new_player,))

    def remove_potential_player(self, player):
        '''
        lobby_info = command
        lobby_info["command_type"] = "LOBBY"
        lobby_info["message"] = "load_next_lvl"
        lobby_info["values"] = ""
        self.send_message_to_player(player, lobby_info)
        '''
        self.lobby_list.remove(player)

    def setup_lobby_player(self, player):
        lobby_info = copy.deepcopy(command_dict)
        lobby_info["command_type"] = "LOBBY"
        lobby_info["message"] = "lobby_count"
        lobby_info["values"] = len(self.lobby_list)
        #this line should be a function call
        self.send_message_to_player(player, lobby_info)

    def send_message_to_player(self, player, message_json):
        print(player["connection"])
        print(player["connection"].send(bytes(json.dumps(message_json), 'UTF-8')))

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
                    print(terminate_thread_flag)
            except:  
                continue

    def execute_command(self, player, message):
        if message["message"] == "enter_game":
            self.command_callback(player, message)
            return True
        return False