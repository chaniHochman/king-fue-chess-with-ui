class SessionManager:
    """
    Manages all active user sessions.

    Responsible only for:
    - storing sessions
    - finding sessions
    - removing expired sessions
    """


    # Initialize session storage.
    def __init__(self):

        self.sessions = {}



    # Add session.
    def add_session(
        self,
        session
    ):
        """
        Store a logged-in session.
        """

        self.sessions[
            session.user.username
        ] = session



    # Find session by username.
    def get_session(
        self,
        username
    ):
        """
        Return session by username.
        """

        return self.sessions.get(
            username
        )



    # Find session by connection.
    def get_by_connection(
        self,
        connection
    ):
        """
        Return session attached
        to a network connection.
        """

        for session in self.sessions.values():

            if session.connection == connection:

                return session


        return None



    # Mark session disconnected.
    def disconnect_session(
        self,
        connection
    ):
        """
        Mark session as disconnected.

        Does not delete it.
        """

        session = self.get_by_connection(
            connection
        )


        if session:

            session.disconnect()


        return session



    # Remove expired session.
    def remove_session(
        self,
        username
    ):
        """
        Permanently remove session.
        """

        self.sessions.pop(
            username,
            None
        )



    # Return all sessions.
    def get_all_sessions(self):
        """
        Return all stored sessions.
        """

        return list(
            self.sessions.values()
        )



    # Check online state.
    def is_online(
        self,
        username
    ):
        """
        Check if user is connected.
        """

        session = self.get_session(
            username
        )


        if session is None:

            return False


        return session.is_connected()

    # Mark session as disconnected.
    def disconnect_session(
        self,
        connection
    ):
        """
        Find session by connection
        and mark it disconnected.
        """

        session = self.get_by_connection(
            connection
        )


        if session is None:
            return None


        session.disconnect()


        return session

    def has_session(
        self,
        username
    ):
        """
        Return True if a session already exists.
        """

        return username in self.sessions