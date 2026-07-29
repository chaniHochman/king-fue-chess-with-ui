import json
import socket
import threading


class TCPClient:
    """
    Client side TCP communication.

    Responsible for:
    - connecting to server
    - sending commands
    - receiving server messages

    Does not know:
    - game logic
    - UI rendering
    - authentication logic
    """


    # Initialize TCP client.
    def __init__(
        self,
        host="localhost",
        port=5000
    ):
        """
        Create socket and initialize state.
        """

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self._host = host

        self._port = port

        self._connected = False

        self.last_message = None



    # Connect to server.
    def connect(
        self
    ):
        """
        Open TCP connection
        and start receiver thread.
        """

        self._socket.connect(
            (
                self._host,
                self._port
            )
        )

        self._connected = True

        self.start_listener()



    # Start receiver thread.
    def start_listener(
        self
    ):
        """
        Listen to server messages
        in background.
        """

        thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )

        thread.start()



    # Send message to server.
    def send_command(
        self,
        command_type,
        data=None
    ):
        """
        Send command as JSON.
        """

        if not self._connected:
            return


        if data is None:
            data = {}


        message = {

            "type": command_type,

            "data": data

        }


        encoded = json.dumps(
            message
        )
        print(
            "CLIENT SEND:",
            message
        )

        self._socket.send(
            encoded.encode("utf-8")
        )



    # Send login request.
    def login(
        self,
        username,
        password
    ):
        """
        Send login command.
        """

        self.send_command(
            "login",
            {
                "username": username,
                "password": password
            }
        )



    # Send register request.
    def register(
        self,
        username,
        password
    ):
        """
        Send register command.
        """

        self.send_command(
            "register",
            {
                "username": username,
                "password": password
            }
        )



    # Search for opponent.
    def play(
        self
    ):
        """
        Send matchmaking request.
        """

        self.send_command(
            "match"
        )



    # Create room.
    def create_room(
        self
    ):
        """
        Send create room request.
        """

        self.send_command(
            "create_room"
        )



    # Join room.
    def join_room(
        self,
        room_id
    ):
        """
        Send join room request.
        """

        self.send_command(
            "join_room",
            {
                "room_id": room_id
            }
        )



    # Leave room.
    def leave_room(
        self
    ):
        """
        Send leave room request.
        """

        self.send_command(
            "leave_room"
        )



    # Send move.
    def send_move(
        self,
        move
    ):
        """
        Send player move.
        """

        self.send_command(
            "move",
            {
                "move": move
            }
        )



    # Receive server messages.
    def receive_messages(
        self
    ):
        """
        Receive messages from server.
        """

        while self._connected:

            try:

                data = self._socket.recv(
                    4096
                )


                if not data:

                    break


                message = json.loads(
                    data.decode("utf-8")
                )


                self.last_message = message


                print(
                    "SERVER:",
                    message
                )


            except Exception as error:

                print(
                    "Receive error:",
                    error
                )

                break



        self._connected = False



    # Get last received message.
    def get_last_message(
        self
    ):
        """
        Return latest server message.
        """

        return self.last_message



    # Close connection.
    def disconnect(
        self
    ):
        """
        Close TCP connection.
        """

        self._connected = False


        try:

            self._socket.close()


        except:

            pass