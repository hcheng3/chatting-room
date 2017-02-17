import wx , sys, socket, select

class Mywin(wx.Frame):
    def __init__(self, parent):
        super(Mywin, self).__init__(parent, size = (500,750))
        self.host = "localhost"
        self.port = 9999
        self.socket = None
        self.basicGUI()
        self.Center()
        self.Show()




    def basicGUI(self):
        panel = wx.Panel(self)

        screen = wx.StaticText(panel,-1,"chating screen",(10,5))
        T1 = wx.TextCtrl(panel, pos = (10,30),size = (480,400))

        screen = wx.StaticText(panel, -1, "clients online ", (10, 437))
        T2 = wx.TextCtrl(panel, pos = (10,460),size =(480,100))
        T3 = wx.TextCtrl(panel, pos = (10,580), size=(480, 100))

        send_button = wx.Button(panel,label="send message",pos =(190,680),size = (120,50))
        # self.Bind(wx.EVT_BUTTON, self.send(T3,self.socket,), send_button)

        hostBox = wx.TextEntryDialog(None, "host", "Host", "")
        if hostBox.ShowModal() == wx.ID_OK:
            self.host = hostBox.GetValue()
            portBox = wx.TextEntryDialog(None, "port", "Port", "")
            if portBox.ShowModal() == wx.ID_OK:
                self.port =int(portBox.GetValue())

                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(2)
                try:
                    self.socket.connect((self.host, self.port))
                except:
                    print 'Unable to connect'
                       # failbox = wx.MessageBox(None,'unable to connect')


                nameBox = wx.TextEntryDialog(None, "nickname","choose a nickname for yourself","")
                if nameBox.ShowModal() == wx.ID_OK:
                    userName = nameBox.GetValue()
                    print str(userName)
                    self.socket.send(str(userName))
                    self.SetTitle('welcome ' + userName)

        T1.AppendText('Connected to remote host. You can start sending messages\n'
        'You pressed Ctrl+C to disconnect\n'
        ' Use @nickname to whisper with the other client\n')

        # while True:
        #     socket_list = [T3.GetValue(), self.socket]
        #
        #     # Get the list sockets which are readable
        #     read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        #
        #     for sock in read_sockets:
        #         if sock == self.socket:
        #             # incoming message from remote server, s
        #             data = self.sock.recv(4096)
        #             if not data:
        #                 print '\nDisconnected from chat server'
        #                 sys.exit()
        #             else:
        #                 T1.AppendText(data)
        #
        #                    # sys.stdout.write(data)
        #                    # sys.stdout.write('[Me] ');
        #                    # sys.stdout.flush()
        #
        #         else:
        #             print "aa"
        #                # user entered a message


    def send(self,text_area,aim_socket,event):
        msg = str(text_area.GetValue)
        aim_socket.send(msg)






if __name__ == "__main__":
    app = wx.App()
    Mywin(None)
    app.MainLoop()