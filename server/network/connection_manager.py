class ConnectionManager:
    """
    Manages all active client connections.

    Responsible for:
    - storing connections
    - adding clients
    - removing clients

    Does not know:
    - users
    - games
    - authentication
    """



    # Initialize connection manager.
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



    # Send message to all clients.
    def broadcast(
        self,
        message
    ):
        """
        Send message to every client.
        """

        for connection in self._connections:

            connection.send(
                message
            )



    # Close all connections.
    def close_all(
        self
    ):
        """
        Close server connections.
        """

        for connection in self._connections:

            connection.close()


        self._connections.clear()