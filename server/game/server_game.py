# שמירת מצב משחק אחד.
# הפעלת GameEngine.

# היא לא אחראית על תקשורת רשת.

class ServerGame:
    """
    Represents one active chess game.

    Stores players,
    game engine and current state.
    """



    # Create a new server game.
    def __init__(
        self,
        room,
        game_engine
    ):

        self.room = room

        self.game_engine = game_engine

        self.finished = False



    # Process a player move.
    def make_move(
        self,
        move
    ):

        if isinstance(move, (tuple, list)) and len(move) == 2:
            source, target = move
            result = self.game_engine.request_move(source, target)
            return result

        result = (
            self.game_engine.request_move(
                move
            )
        )

        return result



    # Check if game ended.
    def is_finished(
        self
    ):

        return self.finished

        # Return current game state.
    def get_snapshot(
        self
    ):
        """
        Return current snapshot
        from game engine.
        """

        return self.game_engine.create_snapshot()