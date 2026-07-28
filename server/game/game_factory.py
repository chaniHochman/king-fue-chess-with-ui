from server.game.server_game import ServerGame
from server.game.game_session import GameSession


class GameFactory:
    """
    Creates complete multiplayer game sessions.

    Responsible only for:
    - creating game engine
    - creating ServerGame
    - creating GameSession

    Does not know:
    - networking
    - database
    - authentication
    - rooms logic
    """


    # Initialize game factory.
    def __init__(
        self,
        bus,
        engine_factory
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._engine_factory = engine_factory



    # Create a complete multiplayer game.
    def create_game(
        self,
        room
    ):
        """
        Create one isolated game session.

        Steps:
        1. Create GameEngine.
        2. Wrap it with ServerGame.
        3. Wrap it with GameSession.
        """


        game_engine = (
            self._engine_factory
            .create_engine()
        )


        server_game = ServerGame(
            room,
            game_engine
        )


        game_session = GameSession(
            room,
            server_game,
            self._bus
        )


        return game_session