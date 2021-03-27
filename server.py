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

    def command_handler(self, conn, command):
        print("gasd")

    def main_loop(self):
        id = -1
        holder = PlayerHolder()
        lobby = Lobby()
        while True:
            conn, addr = self.server.accept()
            id+=1
            lobby.add_potential_player(conn, addr, id, self.command_handler)
            #holder.add_player(conn, addr, id)
        conn.close()
        self.server.close()


server = ServerClass()
server.main_loop()