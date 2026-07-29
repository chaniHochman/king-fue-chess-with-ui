import socket
import threading

from server.network.client_connection import ClientConnection
from server.bus.event import Event
from server.bus.event_type import EventType



class TCPServer:
    """
    TCP server.

    Responsible for:
    - accepting connections
    - creating client connections
    - forwarding messages

    Does not know:
    - authentication
    - rooms
    - games
    """



    # Initialize TCP server.
    def __init__(
        self,
        host,
        port,
        connection_manager,
        bus
    ):
        """
        Store server dependencies.
        """

        self._host = host

        self._port = port

        self._connection_manager = connection_manager

        self._bus = bus

        self._running = False

        self._socket = None



    # Start server.
    def start(
        self
    ):
        """
        Open TCP socket
        and accept clients.
        """

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )


        self._socket.bind(
            (
                self._host,
                self._port
            )
        )


        self._socket.listen()


        self._running = True


        print(
            "Server started:",
            self._host,
            self._port
        )


        while self._running:

            connection, address = self._socket.accept()


            client = ClientConnection(
                connection,
                address,
                self._bus
            )


            self._connection_manager.add(
                client
                        )
            print(
                "PUBLISH CLIENT_MESSAGE EVENT"
            )

            self._bus.publish(

                Event(

                    EventType.CLIENT_CONNECTED,

                    {
                        "connection": client
                    }

                )

            )


            thread = threading.Thread(
                target=client.receive,
                daemon=True
            )


            thread.start()



    # Stop server.
    def stop(
        self
    ):
        """
        Close server safely.
        """

        self._running = False


        if self._socket:

            self._socket.close()