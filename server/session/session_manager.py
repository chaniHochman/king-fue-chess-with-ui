from server.session.session import Session



class SessionManager:
    """
    Stores active sessions.

    Responsible for:
    - adding sessions
    - removing sessions
    - searching sessions

    Does not know:
    - authentication
    - rooms
    - games
    """



    # Initialize manager.
    def __init__(
        self
    ):
        """
        Create session storage.
        """

        self._sessions = {}



    # Add session.
    def add_session(
        self,
        session
    ):
        """
        Store session by connection.
        """
        
        print(f"DEBUG SESSION_MANAGER: add_session - storing session id={id(session)} username={session.user.username if session.user else 'None'} connection={session.connection}")
        print(f"DEBUG SESSION_MANAGER: _sessions dict keys before: {list(self._sessions.keys())}")

        self._sessions[
            session.connection
        ] = session
        
        print(f"DEBUG SESSION_MANAGER: _sessions dict keys after: {list(self._sessions.keys())}")



    # Create session.
    def create_session(
        self,
        connection,
        user
    ):
        """
        Create and store session.
        """

        session = Session(
            connection,
            user
        )


        self.add_session(
            session
        )


        return session



    # Get session by connection.
    def get_session(
        self,
        connection
    ):
        """
        Return session.
        """
        
        result = self._sessions.get(
            connection
        )
        
        print(f"DEBUG SESSION_MANAGER: get_session - connection={connection} returning session id={id(result) if result else 'None'} username={result.user.username if result and result.user else 'None'}")
        
        return result



    # Compatibility function.
    def get_by_connection(
        self,
        connection
    ):
        """
        Alias used by SessionResolver.
        """

        return self.get_session(
            connection
        )



    # Remove session.
    def remove_session(
        self,
        connection
    ):
        """
        Delete session.
        """

        return self._sessions.pop(
            connection,
            None
        )



    # Disconnect session.
    def disconnect_session(
        self,
        connection
    ):
        """
        Mark session disconnected.
        """

        session = self.get_session(
            connection
        )


        if session:

            session.disconnect()



    # Return all sessions.
    def get_all_sessions(
        self
    ):
        """
        Return all sessions.
        """

        return list(
            self._sessions.values()
        )