from server.rooms.player import PlayerRole



class Room:
    """
    Represents game room.

    Responsible for:
    - storing players
    - assigning roles
    - storing viewers

    Does not know:
    - game rules
    - networking
    """



    # Initialize room.
    def __init__(
        self,
        room_id
    ):
        """
        Create empty room.
        """

        self.room_id = room_id

        self.players = []

        self.viewers = []



    # Add session.
    def add_player(
        self,
        session
    ):
        """
        Add player or viewer.
        """

        if len(self.players) == 0:

            self.players.append(
                session
            )

            return PlayerRole.WHITE



        if len(self.players) == 1:

            self.players.append(
                session
            )

            return PlayerRole.BLACK



        self.viewers.append(
            session
        )

        return PlayerRole.VIEWER



    # Remove session.
    def remove_session(
        self,
        session
    ):
        """
        Remove user from room.
        """

        if session in self.players:

            self.players.remove(
                session
            )


        if session in self.viewers:

            self.viewers.remove(
                session
            )



    # Check empty.
    def is_empty(
        self
    ):
        """
        Return if no users exist.
        """

        return (
            len(self.players) == 0
            and
            len(self.viewers) == 0
        )