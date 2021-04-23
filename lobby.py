from _thread import *
import json

command = {
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

    def add_potential_player(self, conn, addr, id):
        new_player = player_dict
        new_player["id"] = id
        new_player["connection"] = conn
        new_player["address"] = addr
        self.lobby_list.append(new_player)  
        print(str(new_player["address"]) + " connected")
        start_new_thread(self.clientthread, (new_player,))

    def remove_potential_player(self, player):
        print(5555)
        lobby_info = command
        lobby_info["command_type"] = "LOBBY"
        lobby_info["message"] = "load_next_lvl"
        lobby_info["values"] = ""
        player.send(bytes(json.dumps(lobby_info), 'UTF-8'))
        self.lobby_list.remove(player)

    def setup_lobby_player(self, player):
        lobby_info = command
        lobby_info["command_type"] = "LOBBY"
        lobby_info["message"] = "lobby_count"
        lobby_info["values"] = len(self.lobby_list)
        #this line should be a function call
        player["connection"].send(bytes(json.dumps(lobby_info), 'UTF-8'))

    def clientthread(self, player):
        self.setup_lobby_player(player)
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
                    print(88888)
                    print(message)
                    if message == "":
                        """message may have no content if the connection  
                        is broken, in this case we remove the connection"""
                        #print("cucu")  
                        print("MESAJ GOL")  
                        self.remove(player["connection"])  
                        continue
                    message = json.loads(message)
                    terminate_thread_flag = self.execute_command(player["connection"], message)
            except:  
                continue

    def execute_command(self, conn, message):
        if message["message"] == "enter_game":
            self.command_callback(conn, message["message"])