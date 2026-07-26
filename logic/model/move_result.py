class MoveResult:
    """
    Represents the result of a requested chess move.
    """

    def __init__(self, success: bool, reason: str):
        """
        Initialize the move result with its success flag and reason.
        """
        self.success = success
        self.reason = reason

    def __bool__(self):
        """
        Return whether the move request succeeded.
        """
        return self.success

    def __repr__(self):
        """
        Return a readable representation for debugging.
        """
        return f"MoveResult(success={self.success}, reason='{self.reason}')"