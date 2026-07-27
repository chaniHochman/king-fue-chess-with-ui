#  לפתוח שרת
#  לקבל לקוח חדש
#  ליצור ClientConnection
#  להעביר הלאה
import socket
import threading

from server.network.client_connection import ClientConnection
from server.bus.event import Event
from server.bus.event_type import EventType



class TCPServer:
    """
    Responsible only for:
    - accepting TCP connections
    - creating ClientConnection
    - publishing client messages

    It does not know:
    - users
    - rooms
    - games
    """


    def __init__(
        self,
        host,
        port,
        connection_manager,
        bus
    ):

        self._host = host
        self._port = port

        self._connection_manager = connection_manager

        self._bus = bus

        self._server_socket = None

        self._running = False



    def start(self):

        self._server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )


        self._server_socket.bind(
            (
                self._host,
                self._port
            )
        )


        self._server_socket.listen()

        self._running = True


        print("Server started")


        while self._running:

            client_socket, address = (
                self._server_socket.accept()
            )


            connection = ClientConnection(
                client_socket
            )


            self._connection_manager.add(
                connection
            )


            thread = threading.Thread(
                target=self._handle_client,
                args=(connection,),
                daemon=True
            )


            thread.start()


    # Handle one client connection.
    def _handle_client(
        self,
        connection
    ):
        """
        Receive messages from one client.

        When client disconnects,
        publish disconnect event.
        """


        while connection.is_connected():

            message = connection.receive()


            if message is None:

                self._bus.publish(

                    Event(

                        EventType.PLAYER_DISCONNECTED,

                        {
                            "connection": connection
                        }

                    )

                )

                break


            self._bus.publish(

                Event(

                    EventType.CLIENT_MESSAGE,

                    {
                        "connection": connection,

                        "message": message
                    }

                )

            )



        # Notify server about disconnect.
        self._bus.publish(

            Event(

                EventType.PLAYER_DISCONNECTED,

                {
                    "connection": connection
                }

            )

        )


        self._connection_manager.remove(
            connection
        )


        connection.close()



    def stop(self):

        self._running = False


        if self._server_socket:

            self._server_socket.close()