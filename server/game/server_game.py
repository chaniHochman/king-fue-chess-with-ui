class ServerGame:
    """
    Represents one running game.

    Responsible for:
    - connecting server with GameEngine
    - sending moves to engine
    - returning game snapshot

    Does not know:
    - networking
    - sessions
    - database
    - matchmaking
    """



    # Initialize server game.
    def __init__(
        self,
        room,
        game_engine
    ):
        """
        Store room and engine.
        """

        self.room = room

        self.game_engine = game_engine



    # Process player move.
    def make_move(
        self,
        move
    ):
        """
        Send move to GameEngine.
        """

        if isinstance(move, (tuple, list)):

            if len(move) == 2:

                source, target = move

                return self.game_engine.request_move(
                    source,
                    target
                )


        return self.game_engine.request_move(
            move
        )



    # Return game snapshot.
    def get_snapshot(
        self
    ):
        """
        Return current game state.
        """

        return self.game_engine.create_snapshot()



    # Check game engine state.
    def is_finished(
        self
    ):
        """
        Ask engine if game ended.
        """

        return self.game_engine.is_game_over()