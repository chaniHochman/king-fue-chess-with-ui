import json

from server.bus.event import Event
from server.bus.event_type import EventType


class ClientConnection:
    """
    Represents one connected client.

    Responsible for:
    - receiving data
    - sending data
    - publishing client messages

    Does not know:
    - authentication
    - rooms
    - games
    """


    # Initialize client connection.
    def __init__(
        self,
        connection,
        address,
        bus
    ):
        """
        Store network connection.
        """

        self._connection = connection

        self._address = address

        self._bus = bus

        self._connected = True



    # Receive data from client.
    def receive(
        self
    ):
        """
        Receive JSON message
        and publish event.
        """

        try:

            data = self._connection.recv(
                4096
            )
            print(
                "SERVER RECEIVED:",
                data.decode("utf-8")
            )

            if not data:

                self.close()

                return None


            message = json.loads(
                data.decode("utf-8")
            )
            print(
                "SERVER RECEIVED FROM SOCKET:",
                message
            )

            self._bus.publish(

                Event(

                    EventType.CLIENT_MESSAGE,

                    {
                        "connection": self,

                        "message": message

                    }

                )

            )


            return message


        except Exception:

            self.close()

            return None



    # Send message to client.
    def send(
        self,
        message
    ):
        """
        Send JSON message.
        """

        if not self._connected:
            return


        try:

            encoded = json.dumps(
                message
            )


            self._connection.send(
                encoded.encode("utf-8")
            )


        except Exception:

            self.close()



    # Check connection state.
    def is_connected(
        self
    ):
        """
        Return connection state.
        """

        return self._connected



    # Close connection.
    def close(
        self
    ):
        """
        Close socket safely.
        """

        self._connected = False


        try:

            self._connection.close()


        except:

            pass