import socket
import select
import sys
from _thread import *
from player_holder import PlayerHolder
from lobby import Lobby

class ServerClass:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.IP_address = "23.95.226.141" 
        self.Port = 65432
        self.server.bind((self.IP_address, self.Port))
        self.server.listen(2)
        self.holder = PlayerHolder()
        self.lobby = Lobby(self.command_handler)

    def command_handler(self, player, command):
        print("command:")
        print(command)
        if command["message"] == "enter_game":
            self.lobby.remove_potential_player(self.lobby, player["connection"])
            print("carbune1")
            self.holder.add_player(player["connection"])     
            print("carbune2")

    def main_loop(self):
        id = -1
        while True:
            conn, addr = self.server.accept()
            id+=1
            self.lobby.add_potential_player(conn, addr, id)
            #holder.add_player(conn, addr, id)
        conn.close()
        self.server.close()


server = ServerClass()
server.main_loop()