# מחלקת Session מייצגת חיבור אחד לשרת.
# היא שומרת:
# המשתמש המחובר
# הסוקט שלו
# האם הוא מחובר
# באיזה חדר הוא נמצא

#מחלקה זו מייצגת משתמש רק בזמן שהוא מחובר 
class Session:
    """
    Represents one connected client.

    Stores temporary runtime information.

    Does not know:
    - database
    - matchmaking
    - networking logic
    """

    # Create new online session.
    def __init__(
        self,
        user,
        connection
    ):
        """
        Store user and active connection.
        """

        self.user = user
        self.connection = connection
        self.room = None
        self.game = None
        self.connected = True

    # Check whether client is online.
    def is_connected(self):
        """
        Return current connection state.
        """

        return self.connected

    # Mark client as disconnected.
    def disconnect(self):
        """
        Mark session as offline.
        """

        self.connected = False

    # Mark client as reconnected.
    def reconnect(
        self,
        connection
    ):
        """
        Attach a new connection.
        """

        self.connection = connection
        self.connected = True