import socket
import threading

from server.network.client_connection import ClientConnection

from server.bus.event import Event
from server.bus.event_type import EventType



class TCPServer:
    """
    Main TCP server.

    Responsible for:
    - accepting clients
    - creating connections
    - publishing network events

    Does not know:
    - authentication
    - games
    - rooms
    """



    # Initialize TCP server.
    def __init__(
        self,
        bus,
        connection_manager,
        host="localhost",
        port=5000
    ):
        """
        Store server settings.
        """

        self._bus = bus

        self._connection_manager = connection_manager

        self._host = host

        self._port = port

        self._running = False



    # Start server.
    def start(
        self
    ):
        """
        Open socket and accept clients.
        """

        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )


        server_socket.bind(
            (
                self._host,
                self._port
            )
        )


        server_socket.listen()


        self._running = True


        while self._running:

            client_socket, address = (
                server_socket.accept()
            )


            connection = ClientConnection(
                client_socket,
                address
            )


            self._connection_manager.add(
                connection
            )


            self._bus.publish(

                Event(

                    EventType.CLIENT_CONNECTED,

                    {
                        "connection":
                        connection
                    }

                )

            )


            thread = threading.Thread(

                target=self.listen_client,

                args=(connection,)

            )


            thread.start()



    # Listen to client messages.
    def listen_client(
        self,
        connection
    ):
        """
        Receive messages from client.
        """

        while connection.is_connected():

            message = connection.receive()


            if message is None:

                break


            self._bus.publish(

                Event(

                    EventType.CLIENT_MESSAGE,

                    {
                        "connection":
                        connection,

                        "message":
                        message
                    }

                )

            )


        self._connection_manager.remove(
            connection
        )


        self._bus.publish(

            Event(

                EventType.CLIENT_DISCONNECTED,

                {
                    "connection":
                    connection
                }

            )

        )