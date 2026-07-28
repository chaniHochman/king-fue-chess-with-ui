class ConnectionManager:
    """
    Stores active client connections.

    Responsible for:
    - adding connections
    - removing connections
    - finding connections

    Does not know:
    - authentication
    - rooms
    - games
    """



    # Initialize connection storage.
    def __init__(
        self
    ):
        """
        Create empty connection list.
        """

        self._connections = []



    # Add new connection.
    def add(
        self,
        connection
    ):
        """
        Store client connection.
        """

        self._connections.append(
            connection
        )



    # Remove connection.
    def remove(
        self,
        connection
    ):
        """
        Remove client connection.
        """

        if connection in self._connections:

            self._connections.remove(
                connection
            )



    # Return all connections.
    def get_all(
        self
    ):
        """
        Return active connections.
        """

        return list(
            self._connections
        )



    # Close all connections.
    def close_all(
        self
    ):
        """
        Close every client socket.
        """

        for connection in self._connections:

            connection.close()


        self._connections.clear()