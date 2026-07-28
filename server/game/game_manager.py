from server.bus.event import Event
from server.bus.event_type import EventType


class GameManager:
    """
    Manages all active multiplayer games.

    Responsible for:
    - creating games
    - storing active games
    - finding games
    - forwarding moves

    Does not know:
    - networking
    - authentication
    - database
    - game engine creation
    """


    # Initialize game manager.
    def __init__(
        self,
        bus,
        game_factory
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._game_factory = game_factory

        self._games = {}

        self.register_events()



    # Register game events.
    def register_events(self):
        """
        Subscribe to game requests.
        """

        self._bus.subscribe(
            EventType.MOVE_REQUESTED,
            self.handle_move_event
        )



    # Create game from room.
    def create_game(
        self,
        room
    ):
        """
        Create new GameSession
        using GameFactory.
        """

        game_session = (
            self._game_factory.create_game(
                room
            )
        )


        self._games[
            room.room_id
        ] = game_session


        return game_session



    # Find game by room id.
    def get_game(
        self,
        room_id
    ):
        """
        Return active game.
        """

        return self._games.get(
            room_id
        )



    # Handle move request event.
    def handle_move_event(
        self,
        event
    ):
        """
        Receive move request
        and forward it.
        """

        session = event.data.get(
            "session"
        )

        move = event.data.get(
            "move"
        )


        if session is None or move is None:
            return None


        room = getattr(
            session,
            "room",
            None
        )


        if room is None:
            return None


        return self.handle_move(
            room.room_id,
            move
        )



    # Execute player move.
    def handle_move(
        self,
        room_id,
        move
    ):
        """
        Forward move to GameSession.
        """

        game = self.get_game(
            room_id
        )


        if game is None:
            return None


        result = game.make_move(
            move
        )


        return result



    # Remove finished game.
    def remove_game(
        self,
        room_id
    ):
        """
        Remove game from active games.
        """

        self._games.pop(
            room_id,
            None
        )