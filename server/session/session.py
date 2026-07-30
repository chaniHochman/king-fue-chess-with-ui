import time


class Session:
    """
    Represents connected user.

    Responsible for:
    - storing user
    - storing connection
    - connection state
    - current room

    Does not know:
    - authentication
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
        Store user connection.
        """

        self.connection = connection

        self.user = user

        self.role = None

        self.room = None

        self.connected = True

        self.disconnect_time = None



    # Disconnect session.
    def disconnect(
        self
    ):
        """
        Mark session disconnected.
        """

        self.connected = False

        self.disconnect_time = time.time()



    # Reconnect session.
    def reconnect(
        self,
        connection
    ):
        """
        Replace old connection.
        """

        self.connection = connection

        self.connected = True

        self.disconnect_time = None



    # Assign room.
    def join_room(
        self,
        room
    ):
        """
        Attach session to room.
        """

        self.room = room



    # Remove room.
    def leave_room(
        self
    ):
        """
        Remove current room.
        """

        self.room = None



    # Check authentication.
    def is_authenticated(
        self
    ):
        """
        Return authentication status.
        """

        return self.user is not None



    # Send message.
    def send(
        self,
        message
    ):
        """
        Send message to client.
        """

        if self.connection:

            self.connection.send(
                message
            )



    # Return username.
    def username(
        self
    ):
        """
        Return username safely.
        """

        if self.user:

            return self.user.username

        return None