#Room מייצגת חדר משחק אחד.
# שמירת המשתמשים בחדר.
# קביעת תפקיד.
# בדיקה האם החדר מלא.
import uuid
from server.common.player import PlayerRole

class Room:
    """
    Represents one game room.

    A room can contain two players
    and any number of viewers.
    """


    # Create a new room.
    def __init__(self):

        self.room_id = str(
            uuid.uuid4()
        )

        self.white_player = None

        self.black_player = None

        self.viewers = []

        self.game_session = None

    # Add a session into the room.
    def add_session(
        self,
        session
    ):

        if self.white_player is None:

            self.white_player = session

            session.room = self

            return PlayerRole.WHITE


        if self.black_player is None:

            self.black_player = session

            session.room = self

            return PlayerRole.BLACK


        self.viewers.append(
            session
        )

        session.room = self

        return PlayerRole.VIEWER



    # Remove a session from the room.
    def remove_session(
        self,
        session
    ):

        if self.white_player == session:

            self.white_player = None

        elif self.black_player == session:

            self.black_player = None

        elif session in self.viewers:

            self.viewers.remove(
                session
            )

        session.room = None



    # Check whether room has two players.
    def is_ready(self):

        return (
            self.white_player is not None
            and
            self.black_player is not None
        )
    # Return all sessions inside the room.
    def get_all_sessions(self):
        """
        Return players and viewers in this room.
        """

        sessions = []

        if self.white_player:
            sessions.append(self.white_player)

        if self.black_player:
            sessions.append(self.black_player)

        sessions.extend(self.viewers)

        return sessions