import time


class Session:
    """
    Represents connected user session.

    Responsible for:
    - storing connection
    - storing user
    - tracking connection state
    - tracking current room

    Does not know:
    - authentication logic
    - games
    - database
    """



    # Initialize session.
    def __init__(
        self,
        connection,
        user=None
    ):
        """
        Store client connection and user.
        """

        self.connection = connection

        self.user = user

        self.room = None

        self.connected = True

        self.disconnect_time = None



    # Mark session disconnected.
    def disconnect(
        self
    ):
        """
        Update disconnect state.
        """

        self.connected = False

        self.disconnect_time = time.time()



    # Restore session connection.
    def reconnect(
        self,
        connection
    ):
        """
        Reconnect existing session.
        """

        self.connection = connection

        self.connected = True

        self.disconnect_time = None



    # Attach user to session.
    def set_user(
        self,
        user
    ):
        """
        Store authenticated user.
        """

        self.user = user



    # Check if user is authenticated.
    def is_authenticated(
        self
    ):
        """
        Return authentication state.
        """

        return self.user is not None



    # Send message to client.
    def send(
        self,
        message
    ):
        """
        Send message through connection.
        """

        if self.connection:

            self.connection.send(
                message
            )