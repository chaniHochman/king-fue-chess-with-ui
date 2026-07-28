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
    - rooms
    - authentication logic
    """



    # Initialize TCP client.
    def __init__(self, host="localhost", port=5000):

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



    # Start background listener.
    def start_listener(
        self
    ):
        """
        Start thread that receives
        messages from server.
        """

        self._listener_thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )


        self._listener_thread.start()



    # Send command to server.
    def send_command(
        self,
        command_type,
        data=None
    ):
        """
        Send JSON message.
        """

        if not self._connected:

            return


        if data is None:

            data = {}



        message = {

            "type":
            command_type,

            "data":
            data
        }



        encoded = json.dumps(
            message
        )


        self._socket.send(
            encoded.encode("utf-8")
        )



    # Login request.
    def login(
        self,
        username,
        password
    ):
        """
        Send login request.
        """

        self.send_command(
            "login",
            {
                "username": username,
                "password": password
            }
        )



    # Register request.
    def register(
        self,
        username,
        password
    ):
        """
        Send register request.
        """

        self.send_command(
            "register",
            {
                "username": username,
                "password": password
            }
        )



    # Search opponent.
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
        Create new room.
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
        Join existing room.
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
        Leave current room.
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
        Listen for server responses.
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