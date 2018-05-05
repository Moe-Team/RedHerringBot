import irc.client


SERVER = "chat.freenode.net"
PORT = 6665
CHANNEL = "##mysteryonline"


class MessageQueue:

    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.insert(0, item)
    
    def dequeue(self):
        return self.items.pop()


class IRCConnection:

    def __init__(self, server, port, channel, username):
        self.reactor = irc.client.Reactor()
        self.username = username
        self.server = server
        self.channel = channel
        self._joined = False
        self.msg_q = MessageQueue()
        self.p_msg_q = MessageQueue()
        self.on_first_join_handler = None
        self.on_join_handler = None
        self.on_users_handler = None
        self.on_disconnect_handler = None
        print("Creating connection.")

        try:
            self.connection = self.reactor.server().connect(self.server, port, username)
        except irc.client.ServerConnectionError:
            print('IRC: Could not connect to server')
            raise

        events = ["welcome", "join", "quit", "pubmsg", "nicknameinuse", "namreply", "privnotice", "privmsg", "pong"]
        for e in events:
            self.connection.add_global_handler(e, getattr(self, "on_" + e))

    def get_msg(self):
        return self.msg_q.dequeue()

    def put_back_msg(self, msg):
        self.msg_q.messages.append(msg)

    def get_pm(self):
        return self.p_msg_q.dequeue()

    def send_msg(self, msg):
        self.connection.privmsg(self.channel, msg)

    def send_mode(self, username, msg):
        self.connection.mode(username, msg)

    def send_ping(self):
        self.connection.ping(self.server)

    def is_connected(self):
        return self._joined

    def process(self):
        print("Processing")
        self.reactor.process_once()

    def on_welcome(self, c, e):
        print("on_welcome")
        if irc.client.is_channel(self.channel):
            c.join(self.channel)
        else:
            raise ChannelConnectionError("Couldn't connect to {}".format(self.channel))

    def on_join(self, c, e):
        print("On_join called")
        if not self._joined:
            self.on_first_join_handler()
        self._joined = True
        # nick = e.source.nick
        # if c.nickname != nick:
        #     self.on_join_handler(nick)

    def on_quit(self, c, e):
        nick = e.source.nick
        # self.on_disconnect_handler(nick)

    def on_pubmsg(self, c, e):
        msg = e.arguments[0]
        self.msg_q.enqueue(msg)

    def on_namreply(self, c, e):
        pass
        # self.on_users_handler(e.arguments[2])

    def on_privnotice(self, c, e):
        pass
        # server_response = e.arguments[0]
        # Logger.info('IRC: {}'.format(server_response))

    def on_nicknameinuse(self, c, e):
        pass

    def on_privmsg(self, c, e):
        msg = e.arguments[0]
        self.p_msg_q.enqueue(msg)

    def on_pong(self, c, e):
        pass
        # self.connection_manager.receive_pong()


def create_irc_connection():
    result = IRCConnection(SERVER, PORT, CHANNEL, "RedHerringBot")
    print("Created irc_connection")
    return result


def create_own_connection(server, port, username):
    irc = IRCConnection(server, port, '##mysteryonline', username)
    return irc

