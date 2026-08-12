import json

from server.messages import Message
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
        Continuously receive messages
        from client socket.
        """

        while self._connected:

            try:

                data = self._connection.recv(
                    4096
                )


                if not data:

                    self.close()

                    break



                text = data.decode(
                    "utf-8"
                )


                print(
                    "SERVER RECEIVED:",
                    text
                )


                message = Message.decode(
                    text.strip()
                )


                self._bus.publish(

                    Event(

                        EventType.CLIENT_MESSAGE,

                        {
                            "connection": self,

                            "message": message.to_dict()

                        }

                    )

                )



            except Exception as error:

                print(
                    "Receive error:",
                    error
                )

                self.close()

                break





    # Send message to client.
    def send(
        self,
        message
    ):
        """
        Send encoded message.

        Accepts:
        - Message object
        - bytes
        - dictionary
        """

        if not self._connected:

            return



        try:


            if isinstance(
                message,
                Message
            ):

                data = message.encode()



            elif isinstance(
                message,
                bytes
            ):

                data = message



            else:

                data = (
                    json.dumps(message)
                    + "\n"
                ).encode("utf-8")



            self._connection.sendall(
                data
            )



        except Exception as error:

            print(
                "Send error:",
                error
            )

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

        if not self._connected:
            return

        self._connected = False

        self._bus.publish(
            Event(
                EventType.CLIENT_DISCONNECTED,
                {
                    "connection": self
                }
            )
        )

        try:

            self._connection.close()


        except:

            pass