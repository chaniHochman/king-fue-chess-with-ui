class MovesLog:
    """
    Stores game moves.

    Responsible for:
    - recording moves
    - returning move history

    Does not know:
    - UI
    - networking
    - database
    """


    # Initialize move storage.
    def __init__(
        self
    ):
        """
        Create empty move list.
        """

        self._moves = []



    # Add new move.
    def add_move(
        self,
        piece,
        source,
        destination
    ):
        """
        Store executed move.
        """


        self._moves.append(
            {
                "piece_id":
                piece.piece_id,

                "piece":
                piece.kind,

                "color":
                piece.color,

                "source":
                (
                    source.row,
                    source.col
                ),

                "destination":
                (
                    destination.row,
                    destination.col
                )
            }
        )



    # Return all moves.
    def get_moves(
        self
    ):
        """
        Return move history.
        """

        return list(
            self._moves
        )