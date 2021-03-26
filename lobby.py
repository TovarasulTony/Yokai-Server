import json

command = {
  "command_type": "INVALID",
  "message": "",
  "values": None
}

class Lobby:
    def __init__(self):
        self.lobby_list = []

    def add_potential_player(self, player, addr, id):
        self.lobby_list.append(player)  
        print (addr[0] + " connected")
        start_new_thread(self.clientthread,(player,addr, id))

    def setup_lobby_player(self, conn):
        lobby_info = command
        lobby_info["command_type"] = "LOBBY"
        lobby_info["message"] = "lobby_count"
        lobby_info["values"] = len(lobby_list)
        conn.send(bytes(json.dumps(lobby_info), 'UTF-8'))

    def clientthread(self, conn, addr, id):
        setup_lobby_player(conn)
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