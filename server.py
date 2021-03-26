import socket
import select
import sys
from _thread import *
from player_holder import PlayerHolder
from lobby import Lobby


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = "23.95.226.141" 
Port = 65432
server.bind((IP_address, Port))
server.listen(2)

id = -1
holder = PlayerHolder()
lobby = Lobby()
while True:
    conn, addr = server.accept()
    id+=1
    lobby.add_potential_player(conn, addr, id)
    #holder.add_player(conn, addr, id)
conn.close()
server.close()