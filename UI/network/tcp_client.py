import json
import socket
import threading


class TCPClient:
    """
    Client side TCP communication.

    Responsible for:
    - connecting to server
    - sending commands
    - receiving messages

    Does not know:
    - game logic
    - UI
    """



    SEPARATOR = "\n"



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


        self._buffer = ""



    # Connect to server.
    def connect(
        self
    ):
        """
        Open connection
        and start receiver.
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
        Start background receiver.
        """

        thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )


        thread.start()



    # Send command.
    def send_command(
        self,
        command_type,
        data=None
    ):
        """
        Send JSON command
        with TCP separator.
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



        encoded = (

            json.dumps(message)

            +

            self.SEPARATOR

        )



        print(
            "CLIENT SEND:",
            message
        )



        self._socket.sendall(

            encoded.encode("utf-8")

        )



    # Receive server messages.
    def receive_messages(
        self
    ):
        """
        Receive messages continuously.

        Uses buffer because TCP
        has no message boundaries.
        """


        while self._connected:


            try:

                data = self._socket.recv(
                    4096
                )



                if not data:

                    break



                self._buffer += data.decode(
                    "utf-8"
                )



                while self.SEPARATOR in self._buffer:


                    raw, self._buffer = self._buffer.split(

                        self.SEPARATOR,

                        1

                    )



                    if not raw:

                        continue



                    message = json.loads(
                        raw
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



    # Get last message.
    def get_last_message(
        self
    ):
        """
        Return the latest message and consume it.

        This method returns the current `last_message` and immediately clears
        the stored value so the same message is not processed repeatedly by
        polling callers. Use this when a single consumer should handle each
        server message exactly once.
        """

        message = self.last_message

        # Consume the message so subsequent calls don't return the same one.
        self.last_message = None

        return message



    # Send login.
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
                "username":
                username,

                "password":
                password
            }

        )



    # Send register.
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
                "username":
                username,

                "password":
                password
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
        Send room creation request.
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
                "room_id":
                room_id
            }

        )



    # Leave room.
    def leave_room(
        self
    ):
        """
        Send leave request.
        """

        self.send_command(
            "leave_room"
        )



    # Send move.
    def send_move(
        self,
        game_id,
        source,
        target
    ):
        """
        Send game move.
        """

        self.send_command(

            "move",

            {
                "game_id": game_id,

                "source": {
                    "row": source.row,
                    "col": source.col
                },

                "target": {
                    "row": target.row,
                    "col": target.col
                }
            }

        )



    # Disconnect.
    def disconnect(
        self
    ):
        """
        Close connection.
        """

        self._connected = False


        try:

            self._socket.close()


        except:

            pass