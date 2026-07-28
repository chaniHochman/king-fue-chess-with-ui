from server.bus.event import Event
from server.bus.event_type import EventType



class SessionManager:
    """
    Manages connected user sessions.

    Responsible for:
    - creating sessions
    - storing sessions
    - removing sessions
    - tracking disconnects

    Does not know:
    - authentication logic
    - rooms
    - games
    - database
    """



    # Initialize session manager.
    def __init__(
        self,
        bus=None
    ):
        """
        Store sessions.
        """

        self._bus = bus

        self._sessions = []



    # Create new session.
    def create_session(
        self,
        connection,
        user=None
    ):
        """
        Create and store session.
        """

        from server.session.session import Session


        session = Session(
            connection,
            user
        )


        self._sessions.append(
            session
        )


        if self._bus:

            self._bus.publish(

                Event(

                    EventType.SESSION_CREATED,

                    {
                        "session":
                        session
                    }

                )

            )


        return session



    # Find session by connection.
    def get_by_connection(
        self,
        connection
    ):
        """
        Return session
        attached to connection.
        """

        for session in self._sessions:

            if session.connection == connection:

                return session


        return None



    # Remove session.
    def remove_session(
        self,
        session
    ):
        """
        Remove session.
        """

        if session in self._sessions:

            self._sessions.remove(
                session
            )


            if self._bus:

                self._bus.publish(

                    Event(

                        EventType.SESSION_REMOVED,

                        {
                            "session":
                            session
                        }

                    )

                )



    # Mark session disconnected.
    def disconnect(
        self,
        session
    ):
        """
        Mark player as disconnected.

        DisconnectMonitor will
        handle timeout.
        """

        session.connected = False



    # Return all sessions.
    def get_all_sessions(
        self
    ):
        """
        Return sessions list.
        """

        return list(
            self._sessions
        )



    # Find session by username.
    def get_by_username(
        self,
        username
    ):
        """
        Return user's session.
        """

        for session in self._sessions:

            if session.user:

                if session.user.username == username:

                    return session


        return None