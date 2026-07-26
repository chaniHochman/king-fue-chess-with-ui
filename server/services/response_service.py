from server.messages import Message

from server.common.message_type import MessageType



class ResponseService:
    """
    Sends server responses to clients.

    Responsible only for:
    - converting events into messages
    - sending messages

    Does not know:
    - authentication logic
    - rooms
    - games
    """



    # Initialize response service.
    def __init__(
        self,
        bus
    ):
        """
        Store message bus
        and register listeners.
        """

        self.bus = bus

        self.register_events()



    # Register response events.
    def register_events(self):
        """
        Subscribe to events
        that require client response.
        """


        from server.bus.event_type import EventType


        self.bus.subscribe(
            EventType.LOGIN_SUCCESS,
            self.login_success
        )


        self.bus.subscribe(
            EventType.LOGIN_FAILED,
            self.login_failed
        )


        self.bus.subscribe(
            EventType.ROOM_CREATED,
            self.room_created
        )


        self.bus.subscribe(
            EventType.ROOM_JOIN_FAILED,
            self.room_join_failed
        )
        self.bus.subscribe(
            EventType.GAME_STARTED,
            self.game_started
        )



    # Send login success message.
    def login_success(
        self,
        event
    ):
        """
        Notify client about successful login.
        """

        connection = event.data["connection"]


        connection.send(
            Message(
                MessageType.LOGIN_SUCCESS,
                {}
            )
        )



    # Send login failed message.
    def login_failed(
        self,
        event
    ):
        """
        Notify client about failed login.
        """

        connection = event.data["connection"]


        connection.send(
            Message(
                MessageType.ERROR,
                {
                    "reason":
                    event.data["reason"]
                }
            )
        )



    # Send created room id.
    def room_created(
        self,
        event
    ):
        """
        Send new room id
        to creator.
        """

        connection = event.data["connection"]


        connection.send(
            Message(
                MessageType.CREATE_ROOM,
                {
                    "room_id":
                    event.data["room_id"]
                }
            )
        )



    # Send join failed response.
    def room_join_failed(
        self,
        event
    ):
        """
        Notify client that room was not found.
        """

        connection = event.data["connection"]


        connection.send(
            Message(
                MessageType.ERROR,
                {
                    "reason":
                    event.data["reason"]
                }
            )
        )
        # Send game start message.
    def game_started(
        self,
        event
    ):
        """
        Notify players that game started.
        """


        white = event.data["white"]

        black = event.data["black"]


        room_id = event.data["room_id"]


        players = [
            event.data["white"],
            event.data["black"]
        ]


        message = Message(
            MessageType.GAME_STARTED,
            {
                "room_id": room_id,

                "white": white,

                "black": black
            }
        )
        
        # Send game start message.
    def send_game_started(
        self,
        event
    ):
        """
        Notify both players
        that game started.
        """


        message = Message(

            MessageType.GAME_STARTED,

            {
                "room_id":
                event.data["room_id"]
            }

        )


        white = event.data["white"]

        black = event.data["black"]



        white.connected.send(
            message
        )


        black.connected.send(
            message
        )