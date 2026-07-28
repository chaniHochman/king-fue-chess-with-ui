from server.bus.event import Event
from server.bus.event_type import EventType


class SessionManager:
    """
    Stores all active user sessions.

    Responsible for:
    - creating sessions
    - removing sessions
    - finding sessions

    Does not know:
    - authentication
    - rooms
    - games
    """


    # Initialize session storage.
    def __init__(
        self
    ):
        """
        Create empty session collection.
        """

        self._sessions = {}



    # Create new session.
    def create_session(
        self,
        connection,
        user
    ):
        """
        Create session after successful login.
        """

        from server.session.session import Session


        session = Session(
            connection,
            user
        )


        self._sessions[connection] = session


        return session



    # Remove session.
    def remove_session(
        self,
        connection
    ):
        """
        Delete disconnected session.
        """

        session = self._sessions.pop(
            connection,
            None
        )


        return session



    # Find session by connection.
    def get_session(
        self,
        connection
    ):
        """
        Return session belonging
        to connection.
        """

        return self._sessions.get(
            connection
        )



    # Return all sessions.
    def get_all_sessions(
        self
    ):
        """
        Return active sessions.
        """

        return list(
            self._sessions.values()
        )