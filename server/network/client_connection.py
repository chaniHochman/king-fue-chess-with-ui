import socket


class ClientConnection:
    """
    Represents one client connection.

    Responsible for:
    - receiving messages
    - sending messages
    - closing connection

    Does not know:
    - authentication
    - rooms
    - games
    - database
    """



    # Initialize client connection.
    def __init__(
        self,
        socket,
        address
    ):
        """
        Store socket information.
        """

        self._socket = socket

        self.address = address

        self._connected = True



    # Receive message from client.
    def receive(
        self
    ):
        """
        Read data from socket.
        """

        try:

            data = self._socket.recv(
                4096
            )


            if not data:

                self._connected = False

                return None


            return data.decode(
                "utf-8"
            )


        except:

            self._connected = False

            return None



    # Send message to client.
    def send(
        self,
        message
    ):
        """
        Send text message.
        """

        if not self._connected:

            return


        try:

            self._socket.send(
                message.encode(
                    "utf-8"
                )
            )


        except:

            self._connected = False



    # Check connection status.
    def is_connected(
        self
    ):
        """
        Return connection state.
        """

        return self._connected



    # Close client connection.
    def close(
        self
    ):
        """
        Close socket.
        """

        self._connected = False


        try:

            self._socket.close()


        except:

            pass