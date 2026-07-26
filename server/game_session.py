class GameSession:
    """
    Represents one running game.

    Responsible for:
    - connecting players to a game
    - holding GameEngine
    - controlling game state

    Does not handle:
    - networking
    - authentication
    - rooms
    """

    # Create a new game session.
    def __init__(
        self,
        game_engine
    ):

        self.game_engine = game_engine

        self.white_player = None

        self.black_player = None


    # Add player to game.
    def add_player(
        self,
        session,
        role
    ):
        """
        Attach player according
        to assigned room role.
        """

        if role == "WHITE":

            self.white_player = session


        elif role == "BLACK":

            self.black_player = session



    # Check whether game can start.
    def is_ready(
        self
    ):
        """
        Return True when
        both players joined.
        """

        return (
            self.white_player is not None
            and
            self.black_player is not None
        )


    # Execute player move.
    def make_move(
        self,
        source,
        target
    ):
        """
        Send move request
        to existing GameEngine.
        """

        return self.game_engine.request_move(
            source,
            target
        )


    # Return current game snapshot.
    def get_snapshot(
        self
    ):
        """
        Return current game state
        for clients.
        """

        return self.game_engine.create_snapshot()