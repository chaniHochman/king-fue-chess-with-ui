class ScoreData:
    """
    Stores game score information.

    Responsible for:
    - tracking captures
    - calculating game points

    Does not know:
    - UI
    - rendering
    - networking
    """


    # Initialize score storage.
    def __init__(
        self
    ):
        """
        Create empty score data.
        """

        self._captures = {}



    # Add captured piece.
    def add_capture(
        self,
        piece
    ):
        """
        Store captured piece value.
        """


        color = piece.color


        if color not in self._captures:

            self._captures[color] = 0


        self._captures[color] += 1



    # Return score.
    def get_score(
        self
    ):
        """
        Return current score.
        """

        return dict(
            self._captures
        )