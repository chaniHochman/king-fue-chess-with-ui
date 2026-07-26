# מחלקה זו אחראית אך ורק על התקשורת עם לקוח אחד.
from server.messages import Message


class ClientConnection:
    """
    Represents one client network connection.

    Responsible only for communication
    with one client.
    """


    # Creates a new client connection object.
    def __init__(self, socket):

        self._socket = socket
        self._connected = True



    # Receives a message from the client.
    def receive(self):

        try:

            data = self._socket.recv(4096)

            if not data:
                self._connected = False
                return None


            return Message.from_json(
                data.decode()
            )


        except Exception:

            self._connected = False
            return None



    # Sends a message to the client.
    def send(self, message):

        if not self._connected:
            return

        self._socket.sendall(
            message.to_json().encode()
        )

    # Checks whether client is connected.
    def is_connected(self):

        return self._connected



    # Closes the client connection.
    def close(self):

        self._connected = False

        self._socket.close()