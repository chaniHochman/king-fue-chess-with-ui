from server.bus.event_type import EventType


class SessionDisconnectService:
    """
    Handles client disconnection.

    Responsible for:
    - finding session
    - marking session disconnected

    Does not know:
    - network
    - rooms
    - games
    """


    # Initialize disconnect service.
    def __init__(
        self,
        bus,
        session_manager
    ):
        """
        Store dependencies
        and register events.
        """

        self._bus = bus

        self._session_manager = session_manager

        self.register_events()



    # Register disconnect listener.
    def register_events(self):
        """
        Subscribe to disconnect events.
        """

        self._bus.subscribe(

            EventType.PLAYER_DISCONNECTED,

            self.handle_disconnect

        )



    # Handle player disconnect.
    def handle_disconnect(
        self,
        event
    ):
        """
        Mark session as disconnected.
        """

        connection = event.data["connection"]


        self._session_manager.disconnect_session(
            connection
        )