from server.bus.event_type import EventType



class SessionDisconnectService:
    """
    Handles user disconnection.

    Responsible for:
    - finding session
    - marking disconnected

    Does not know:
    - games
    - rooms
    - network details
    """



    # Initialize service.
    def __init__(
        self,
        bus,
        session_manager
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._session_manager = session_manager

        self.register_events()



    # Register listener.
    def register_events(
        self
    ):
        """
        Subscribe to disconnect.
        """

        self._bus.subscribe(
            EventType.CLIENT_DISCONNECTED,
            self.handle_disconnect
        )



    # Handle disconnect.
    def handle_disconnect(
        self,
        event
    ):
        """
        Mark session offline.
        """

        connection = event.data["connection"]


        self._session_manager.disconnect_session(
            connection
        )