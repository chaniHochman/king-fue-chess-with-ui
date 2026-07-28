from server.bus.event import Event
from server.bus.event_type import EventType


class GameService:
    """
    Handles game lifecycle.

    Responsible for:
    - starting games
    - forwarding moves
    - handling timeout

    Does not know:
    - networking
    - database
    - authentication
    - game engine creation
    """


    # Initialize game service.
    def __init__(
        self,
        bus,
        game_manager,
        room_manager,
        engine_factory
    ):
        """
        Store dependencies
        and register listeners.
        """

        self._bus = bus

        self._game_manager = game_manager

        self._room_manager = room_manager

        self._engine_factory = engine_factory

        self.register_events()



    # Register game events.
    def register_events(self):
        """
        Subscribe to game events.
        """

        self._bus.subscribe(
            EventType.GAME_CREATED,
            self.start_game
        )


        self._bus.subscribe(
            EventType.MOVE_REQUESTED,
            self.handle_move
        )


        self._bus.subscribe(
            EventType.PLAYER_TIMEOUT,
            self.handle_timeout
        )



    # Create game after room is ready.
    def start_game(
        self,
        event
    ):
        """
        Create new game session.
        """

        room_id = event.data["room_id"]


        room = self._room_manager.get_room(
            room_id
        )


        if room is None:
            return


        game = self._game_manager.create_game(
            room
        )


        return game



    # Handle player move.
    def handle_move(
        self,
        event
    ):
        """
        Forward move to GameManager.
        """

        session = event.data.get(
            "session"
        )

        move = event.data.get(
            "move"
        )


        if session is None:
            return


        if move is None:
            return


        if session.room is None:
            return


        self._game_manager.handle_move(
            session.room.room_id,
            move
        )



    # Handle player timeout.
    def handle_timeout(
        self,
        event
    ):
        """
        Finish game after timeout.
        """

        session = event.data.get(
            "session"
        )


        if session is None:
            return


        if session.room is None:
            return


        room_id = session.room.room_id


        game = self._game_manager.get_game(
            room_id
        )


        if game is None:
            return


        game.finish()


        self._bus.publish(
            Event(
                EventType.GAME_FINISHED,
                {
                    "room_id": room_id,
                    "reason": "timeout"
                }
            )
        )



    # Return game snapshot.
    def get_snapshot(
        self,
        room_id
    ):
        """
        Return current game state.
        """

        game = self._game_manager.get_game(
            room_id
        )


        if game is None:
            return None


        return game.get_snapshot()