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

        self.game_id = None

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
        
        print(f"DEBUG ROOM: add_player called with session id={id(session)} username={session.username() if hasattr(session, 'username') else 'NO_USERNAME_METHOD'}")

        if len(self.players) == 0:

            self.players.append(
                session
            )
            print(f"DEBUG ROOM: Added as WHITE. players list now: {[p.username() for p in self.players if hasattr(p, 'username')]}")

            return PlayerRole.WHITE



        if len(self.players) == 1:

            self.players.append(
                session
            )
            print(f"DEBUG ROOM: Added as BLACK. players list now: {[p.username() for p in self.players if hasattr(p, 'username')]}")

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