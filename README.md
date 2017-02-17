# chatting-room

This is a project using socket programming technique to create a chat program based on client-server model using Python programming language.

In the program, we have two major parts, server and the clients.

For server, it is like the intermediate message transportation of different clients, it could broadcast any message from a client to the other participants like a chatting room, and also could help different clients whisper to each other, besides that, it could also enable different clients to choose their nickname, and duplicate nicknames will be handled before the real massage transportation is happened, plus it could also handles and show the current connected clients and disconnect clients, this information also broadcast to all the clients, so every client knows who is online, who is offline . 

For client, once it connects to the server, it could choose the nickname, and begin sending the message, user could either choose whispering to another client or broadcast to everyone the message, and they could choose to disconnect to server by themselves.

For both server and clients, the technique details will  be discussed in detail design section.


For server:
As you could see in the code part, a class named server is created which include all the information using for creating the server, then a function named run_server will handle the connections between server and clients. 

In the server class initialization, we specify the host, port, receive_buffer, other than that, there are two variables. one is socketlist, another is nicknames.

The list socketlist is used for handling and storing all the clients sockets when connecting to the server, and it provide select.select() a resource to get the ready to read socket.

The dictionary nicknames is used for storing all the nickname for each client, it using the nickname for client as key to store their socket, using this nickname, socket pair could not just helps the server tell whether there is a duplicate nickname when the client wants to connect to the server, it also could enable client using nickname to whisper with aimed client.

Except the basic function of the server socket like creating ,setting, binding , listening and accepting. the stuff worth mention for server is the usage of select.select(potential_readers, potential_writers,potential_errs, timeout), the potential_readers contain all the sockets we may want to try to read from,the other two means all sockets we may want to write to and the ones we want to check for error, and the last one timeout, I set it to 0 to make it a non-blocking mode, which means it will poll but never block.
In the project, we only focused on the socket we could read when its readable means there are some clients send a message, so the select() function  monitor all the clients socket and also server socket(the accept() function of the server socket) for readability.

Other than that, I used a while loop for the server to accept, receive and send message through sockets. 

At first, the program check whether there are new connection to the server socket, if there is, the server check for whether there is a nickname duplication, if not the server will build the connection and broadcast to all the clients, if there is, the server will told the client there is duplicate nickname then close the socket.all the connection and disconnection information will be showed in the the server.

Then, after checking for the server socket, the program will check the client socket, either receive the data from the client socket, then decide whether do the broadcast or whisper. in the process, the try and except statement are used for catching those exceptions when trying to send or receive the data. in here, when the broadcast is clear, for the whisper, the program will check if the data begin with @clientnickname ,if it is, the program will use the nickname dict mentioned before to find the aimed client, then send the message.

Those are the important details of the server side in programming detail, other than those are trivial.

For client:
In client side, things are simpler compared with server side, except the same creating connect the socket work, a very simple GUI are created for entering the host port and nickname for the client. other than that we also used select.select() function to control between receive data from server and send data to server.

For the GUI part, I tried a complicate one for client, but failed, So I give up and only using the simple one to get the host,port and nickname.

the usage of  select.select() and sys.stdin inside of while loop means we check data receiving  from server first, and when I my message typing is complete and ready to send(which means I entered the ?enter ?in bash),  the program will send my message. in this way, it granted that the concurrency between sending and  receiving message for client. because when I typing my message, as long as I didn't finish which mean the sys.stdin is not ready and readable, but the socket is readable(which means there is message coming in from the server side )the while loop still running to receiving the message. and when I am finish typing , and there is no message coming in, my message will be send, if both of the sys.stdin and socket becomes readable, the while loop will at first receive the message then send the message. but there is a little problem in the implementation, so the something wrong with the concurrency, which I will talk detailed in next section.
those are the important part of the client side. I will add the UI I tried to make in the end of the report
