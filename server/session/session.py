import time


class Session:
    """
    Represents one logged-in user session.

    Responsible for:
    - storing user information
    - storing current connection
    - tracking room
    - handling reconnect state

    Does not know:
    - authentication
    - games
    - database
    """


    # Create user session.
    def __init__(
        self,
        user,
        connection
    ):
        """
        Initialize session data.
        """

        self.user = user

        self.connection = connection

        self.room = None

        self.connected = True

        self.disconnect_time = None



    # Replace network connection.
    def reconnect(
        self,
        connection
    ):
        """
        Attach a new client connection
        to this existing session.
        """

        self.connection = connection

        self.connected = True

        self.disconnect_time = None



    # Mark session as disconnected.
    def disconnect(self):
        """
        Mark user as temporarily disconnected.
        """

        self.connected = False

        self.disconnect_time = time.time()



    # Check if session is connected.
    def is_connected(self):
        """
        Return connection state.
        """

        return self.connected



    # Check reconnect timeout.
    def disconnected_seconds(
        self
    ):
        """
        Return how long the user
        has been disconnected.
        """

        if self.disconnect_time is None:

            return 0


        return time.time() - self.disconnect_time

    

        # Check reconnect availability.
    def can_reconnect(
        self,
        timeout=20
    ):
        """
        Return True if user can reconnect
        before timeout expires.
        """

        if self.connected:

            return False


        return (
            self.disconnected_seconds()
            <= timeout
        )