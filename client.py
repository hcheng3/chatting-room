import sys, socket, select, wx, time

class chat_client(wx.Frame):
    # the initiate of the client
    def __init__(self):
        self.host = "host"
        self.port = 9999
        self.socket = None
        self.userName = None
        self.client_run()

    def client_run(self):
        # UI for the enter of the host,port,and nickname
        hostBox = wx.TextEntryDialog(None, "host", "Host", "")
        if hostBox.ShowModal() == wx.ID_OK:
            self.host = hostBox.GetValue()
        hostBox.Destroy()
        portBox = wx.TextEntryDialog(None, "port", "Port", "")
        if portBox.ShowModal() == wx.ID_OK:
            self.port = int(portBox.GetValue())
        portBox.Destroy()

                # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # self.socket.settimeout(2)
                # try:
                #     self.socket.connect((self.host, self.port))
                # except:
                #     print 'Unable to connect'

        nameBox = wx.TextEntryDialog(None, "nickname", "choose a nickname for yourself", "")
        if nameBox.ShowModal() == wx.ID_OK:
            self.userName = nameBox.GetValue()
        nameBox.Destroy()


        #  creating and conncecting the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        try:
            self.socket.connect((self.host, self.port))
        except:
            print 'Unable to connect'
        #  at first connected and send the nickname, if no duplicate in server,it connected, if it is connection wil stoped
        print "choose a nickname for yourself"
        sys.stdout.flush()
        self.userName = sys.stdin.readline()
        self.socket.send(str(self.userName))

        print 'Connected to remote host. You can start sending messages'
        print 'You pressed Ctrl+C to disconnect'
        print ' Use @nickname to whisper with the other client'
        sys.stdout.write('[Me] ');sys.stdout.flush()

        while True:

            socket_list = [sys.stdin, self.socket]

            #  using select.select() to get the ready to read object,either the message we typed in or the socket receive message
            # from server
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

            for sock in read_sockets:
                if sock == self.socket:

                    data = sock.recv(4096)
                    if not data:
                        print 'Disconnected from chat server\n'
                        sys.exit()
                    else:

                        sys.stdout.write(data)
                        sys.stdout.write('[Me] ');sys.stdout.flush()

                else:

                    msg = sys.stdin.readline()
                    # using for texting concurrency although its not working as expected
                    # while True:
                    #     self.socket.send(msg)
                    #     time.sleep(10)

                    self.socket.send(msg)
                    sys.stdout.write('[Me] ');
                    sys.stdout.flush()

if __name__ == "__main__":
    app = wx.App()
    chat_client()
    app.MainLoop()