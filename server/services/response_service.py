from server.messages import Message
from server.common.message_type import MessageType
from server.bus.event_type import EventType


class ResponseService:
    """
    Sends server events
    back to clients.

    Responsible for:
    - converting events to messages
    - sending messages

    Does not know:
    - game rules
    - database
    """


    # Initialize response service.
    def __init__(
        self,
        bus
    ):
        """
        Store bus.
        """

        self._bus = bus

        self.register_events()



    # Register response events.
    def register_events(self):
        """
        Subscribe to outgoing events.
        """

        self._bus.subscribe(
            EventType.LOGIN_SUCCESS,
            self.send_login_success
        )


        self._bus.subscribe(
            EventType.LOGIN_FAILED,
            self.send_error
        )


        self._bus.subscribe(
            EventType.GAME_STARTED,
            self.send_game_started
        )


        self._bus.subscribe(
            EventType.GAME_STATE_CHANGED,
            self.send_game_state
        )


        self._bus.subscribe(
            EventType.MOVE_ACCEPTED,
            self.send_move_result
        )


        self._bus.subscribe(
            EventType.MOVE_REJECTED,
            self.send_move_result
        )


        self._bus.subscribe(
            EventType.GAME_FINISHED,
            self.send_game_finished
        )



    # Send login success.
    def send_login_success(
        self,
        event
    ):
        """
        Notify successful login.
        """

        connection = event.data["connection"]


        connection.send(
            Message(
                MessageType.LOGIN,
                {
                    "success":
                    True
                }
            )
        )



    # Send error.
    def send_error(
        self,
        event
    ):
        """
        Send error message.
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



    # Send game started.
    def send_game_started(
        self,
        event
    ):
        """
        Notify players game started.
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



    # Send game snapshot.
    def send_game_state(
        self,
        event
    ):
        """
        Send current board state.
        """

        room_id = event.data["room_id"]

        snapshot = event.data["snapshot"]


        message = Message(
            MessageType.GAME_STATE,
            {
                "room_id":
                room_id,

                "snapshot":
                snapshot
            }
        )


        players = event.data.get(
            "players",
            []
        )


        for player in players:

            player.connected.send(
                message
            )



    # Send move result.
    def send_move_result(
        self,
        event
    ):
        """
        Notify about move result.
        """

        pass



    # Send game finished.
    def send_game_finished(
        self,
        event
    ):
        """
        Notify game ended.
        """

        pass