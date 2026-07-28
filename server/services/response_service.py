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
    - game logic
    - database
    - authentication
    """



    # Initialize response service.
    def __init__(
        self,
        bus
    ):
        """
        Store bus and register events.
        """

        self._bus = bus

        self.register_events()



    # Register response events.
    def register_events(
        self
    ):
        """
        Subscribe to events
        that require client response.
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
            EventType.ROOM_CREATED,
            self.room_created
        )

        self._bus.subscribe(
            EventType.ROOM_JOIN_FAILED,
            self.room_join_failed
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

        self._bus.subscribe(
            EventType.SCORE_UPDATED,
            self.score_updated
        )

        self._bus.subscribe(
            EventType.PLAY_SOUND,
            self.play_sound
        )

        self._bus.subscribe(
            EventType.PLAY_ANIMATION,
            self.play_animation
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
            ).encode()
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
            ).encode()
        )



    # Send room created.
    def room_created(
        self,
        event
    ):
        """
        Return new room id.
        """

        connection = event.data["connection"]

        connection.send(
            Message(
                MessageType.ROOM_CREATED,
                {
                    "room_id":
                    event.data["room_id"]
                }
            ).encode()
        )



    # Send room join failure.
    def room_join_failed(
        self,
        event
    ):
        """
        Notify room join failure.
        """

        connection = event.data["connection"]

        connection.send(
            Message(
                MessageType.ERROR,
                {
                    "reason":
                    event.data.get("reason")
                }
            ).encode()
        )



    # Send game started.
    def game_started(
        self,
        event
    ):
        """
        Notify players that game started.
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


        white.connection.send(
            message
        )


        black.connection.send(
            message
        )



    # Send accepted move.
    def move_accepted(
        self,
        event
    ):
        """
        Notify clients about valid move.
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
        Notify client about invalid move.
        """

        connection = event.data.get(
            "connection"
        )


        if connection is None:

            return


        connection.send(
            Message(
                MessageType.ERROR,
                {
                    "reason":
                    "invalid_move"
                }
            ).encode()
        )



    # Send game state.
    def game_state_changed(
        self,
        event
    ):
        """
        Send updated snapshot.
        """

        self.broadcast_room(
            event,
            Message(
                MessageType.GAME_STATE,
                {
                    "snapshot":
                    event.data["snapshot"]
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



    # Send score update.
    def score_updated(
        self,
        event
    ):
        """
        Send new rating.
        """

        self.broadcast_room(
            event,
            Message(
                MessageType.SCORE_UPDATE,
                {
                    "winner":
                    event.data.get("winner_rating"),

                    "loser":
                    event.data.get("loser_rating")
                }
            )
        )



    # Send sound request.
    def play_sound(
        self,
        event
    ):
        """
        Tell client to play sound.
        """

        self.broadcast_room(
            event,
            Message(
                MessageType.PLAY_SOUND,
                {
                    "sound":
                    event.data["sound"]
                }
            )
        )



    # Send animation request.
    def play_animation(
        self,
        event
    ):
        """
        Tell client to play animation.
        """

        self.broadcast_room(
            event,
            Message(
                MessageType.PLAY_ANIMATION,
                event.data
            )
        )



    # Send message to room players.
    def broadcast_room(
        self,
        event,
        message
    ):
        """
        Send message to all players
        from event room.
        """

        players = event.data.get(
            "players"
        )


        if players is None:

            return


        for player in players:

            player.connection.send(
                message
            )