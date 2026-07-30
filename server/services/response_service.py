from server.messages import Message
from server.common.message_type import MessageType
from server.bus.event_type import EventType



class ResponseService:
    """
    Sends server responses to clients.

    Responsible for:
    - converting events into messages
    - sending messages

    Does not know:
    - authentication
    - rooms
    - games
    """



    # Initialize response service.
    def __init__(
        self,
        bus
    ):
        """
        Store bus reference.
        """

        self._bus = bus

        self.register_events()



    # Register response events.
    def register_events(
        self
    ):
        """
        Subscribe to response events.
        """


        self._bus.subscribe(
            EventType.LOGIN_SUCCESS,
            self.login_success
        )


        self._bus.subscribe(
            EventType.LOGIN_FAILED,
            self.login_failed
        )


        self._bus.subscribe(
            EventType.REGISTER_SUCCESS,
            self.register_success
        )


        self._bus.subscribe(
            EventType.REGISTER_FAILED,
            self.register_failed
        )


        self._bus.subscribe(
            EventType.ROOM_CREATED,
            self.room_created
        )


        self._bus.subscribe(
            EventType.GAME_STARTED,
            self.game_started
        )


        self._bus.subscribe(
            EventType.MOVE_ACCEPTED,
            self.move_accepted
        )


        self._bus.subscribe(
            EventType.MOVE_REJECTED,
            self.move_rejected
        )


        self._bus.subscribe(
            EventType.GAME_STATE_CHANGED,
            self.game_state_changed
        )


        self._bus.subscribe(
            EventType.GAME_FINISHED,
            self.game_finished
        )



    # Send login success.
    def login_success(
        self,
        event
    ):
        """
        Notify client login succeeded.
        """

        connection = event.data["connection"]


        connection.send(

            Message(

                MessageType.LOGIN_SUCCESS,

                {}

            )

        )



    # Send login failure.
    def login_failed(
        self,
        event
    ):
        """
        Notify client login failed.
        """

        connection = event.data["connection"]


        connection.send(

            Message(

                MessageType.ERROR,

                {
                    "reason":
                    event.data.get("reason")
                }

            )

        )



    # Send register success.
    def register_success(
        self,
        event
    ):
        """
        Notify registration success.
        """

        connection = event.data["connection"]


        connection.send(

            Message(

                MessageType.REGISTER_SUCCESS,

                {}

            )

        )



    # Send register failure.
    def register_failed(
        self,
        event
    ):
        """
        Notify registration failure.
        """

        connection = event.data["connection"]


        connection.send(

            Message(

                MessageType.ERROR,

                {
                    "reason":
                    event.data.get("reason")
                }

            )

        )



    # Send room created.
    def room_created(
        self,
        event
    ):
        """
        Send created room id.
        """

        connection = event.data.get(
            "connection"
        )


        if connection is None:

            return


        connection.send(

            Message(

                MessageType.ROOM_CREATED,

                {
                    "room_id":
                    event.data["room_id"]
                }

            )

        )



    # Send game started.
    def game_started(
        self,
        event
    ):
        """
        Notify players.
        """

        message = Message(

            MessageType.GAME_STARTED,

            {
                "room_id":
                event.data.get("room_id")
            }

        )


        players = event.data.get(
            "players",
            []
        )


        for player in players:

            player.connection.send(
                message
            )



    # Send accepted move.
    def move_accepted(
        self,
        event
    ):
        """
        Broadcast valid move.
        """

        self.broadcast_room(

            event,

            Message(

                MessageType.MOVE,

                {
                    "move":
                    event.data["move"]
                }

            )

        )



    # Send rejected move.
    def move_rejected(
        self,
        event
    ):
        """
        Notify invalid move.
        """

        connection = event.data.get(
            "connection"
        )


        if connection:

            connection.send(

                Message(

                    MessageType.ERROR,

                    {
                        "reason":
                        "invalid_move"
                    }

                )

            )



    # Send game state.
    def game_state_changed(
        self,
        event
    ):
        """
        Send board snapshot.
        """

        self.broadcast_room(

            event,

            Message(

                MessageType.GAME_STATE,

                {
                    "snapshot":
                    event.data.get("snapshot")
                }

            )

        )



    # Send game finished.
    def game_finished(
        self,
        event
    ):
        """
        Notify game ended.
        """

        self.broadcast_room(

            event,

            Message(

                MessageType.GAME_ENDED,

                {
                    "reason":
                    event.data.get("reason")
                }

            )

        )



    # Send message to room players.
    def broadcast_room(
        self,
        event,
        message
    ):
        """
        Send message to all room players.
        """

        players = event.data.get(
            "players",
            []
        )


        for player in players:

            player.connection.send(
                message
            )