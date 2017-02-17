import socket, select

class server():
    # the initiate of the class server
    def __init__(self):
        self.host = 'localhost'
        # used for store all the sockets, include socket for the server side
        self.socketlist = []
        self.receive_buffer = 4096
        self.port = 9999
        # used for store all the nickname of the clients and socket pair
        self.nicknames = {}

    def run_server(self):
        # creating socket and binding socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print "server for chatting program is started on port " + str(self.port)

        self.socketlist.append(server_socket)

        while True:
            # the usage of select.select() function is trying to find all the sockets which are ready and readable
            # then store them in the ready_to_read list
            ready_to_read, ready_to_write, in_error = select.select(self.socketlist, [], [], 0)

            for sock in ready_to_read:
                # if its server side socket,server will continue accept new connected client
                if sock == server_socket:
                    sock_cli, addr = server_socket.accept()
                    # check the nickname of those new connected client,if the nickname is already in the dict,
                    # send back the error message and close the socket

                    nickname = sock_cli.recv(4096)
                    nickname = nickname.replace("\n", "")

                    if self.nicknames.has_key(nickname):
                        sock_cli.send("duplicate nickname,please restart it and choose another nickname\n")
                        sock_cli.close()
                        continue
                    self.nicknames[nickname] = sock_cli
                    #  store the new connected soket in the socketlist
                    self.socketlist.append(sock_cli)
                    print "Client (%s, %s) connected to server" % addr

                    # notify the every clients the join of new client
                    self.broadcast(sock_cli, server_socket, "[%s] entered our chatting room\n" % nickname)
                else:
                    try:
                        data = sock.recv(self.receive_buffer)
                        if data:
                            # check whether the data start with @, if it is its a aimed whisper,if not, go the broadcast
                            # way
                            if data.startswith("@"):

                                target = data.split(" ")[0].replace("@", "")
                                if self.nicknames.has_key(target):

                                    target_sock = self.nicknames.get(target)

                                    name = [key for key, value in self.nicknames.iteritems() if value == sock][0]
                                    target_sock.send("\r" + '[' + name + '] ' + data)
                                else:
                                    sock.send("no such client exist\n")
                            else:
                                # not a whisper, broadcast the message
                                name = [key for key, value in self.nicknames.iteritems() if value == sock][0]
                                self.broadcast(sock,server_socket, "\r" + '[' + name + '] ' + data)
                        else:
                            # no data receive from the socket, so close it and update the socketlist and nickname dict
                            sock.close()
                            if sock in self.socketlist:
                                self.socketlist.remove(sock)

                            name = [key for key, value in self.nicknames.iteritems() if value == sock][0]

                            print "Client (%s, %s) disconnected" % addr

                            self.broadcast(sock,server_socket, "Client [%s] is offline\n" % name)
                            del self.nicknames[name]


                    except:
                        name = [key for key, value in self.nicknames.iteritems() if value == sock][0]
                        self.broadcast(server_socket, sock, "Client [%s] is offline\n" % name)
                        del self.nicknames[name]
                        continue

        server_socket.close()
    # function used for broadcast message to all clients except the server itself and the sender
    def broadcast(self, socket_self, server_socket, message):
        for sock in self.socketlist:
            if sock != server_socket and sock != socket_self:
                try:
                    sock.send(message)
                except:
                    sock.close()
                    if sock in self.socketlist:
                        self.socketlist.remove(sock)



if __name__ == "__main__":
    chat_server = server()
    chat_server.run_server()



