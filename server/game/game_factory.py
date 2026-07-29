from server.game.server_game import ServerGame


class GameFactory:
    """
    Creates ServerGame objects.

    Responsible for:
    - creating new games

    Does not know:
    - rooms
    - players
    - matchmaking
    """



    # Initialize game factory.
    def __init__(
        self,
        bus,
        game_engine_factory
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._game_engine_factory = game_engine_factory



    # Create new server game.
    def create_game(
        self,
        game_id
    ):
        """
        Build new ServerGame.
        """


        engine = self._game_engine_factory.create_engine()



        game = ServerGame(

            game_id,

            engine,

            self._bus

        )


        return game