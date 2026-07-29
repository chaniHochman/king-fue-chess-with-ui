from server.bus.event import Event
from server.bus.event_type import EventType



class ReconnectService:
    """
    Restores disconnected sessions.

    Responsible for:
    - finding previous session
    - attaching new connection

    Does not know:
    - games
    - rooms
    - database
    """



    # Initialize service.
    def __init__(
        self,
        bus,
        session_manager
    ):
        self._bus = bus

        self._session_manager = session_manager

        self.register_events()



    # Register events.
    def register_events(
        self
    ):
        self._bus.subscribe(
            EventType.RECONNECT_REQUEST,
            self.handle_reconnect
        )



    # Handle reconnect.
    def handle_reconnect(
        self,
        event
    ):
        """
        Restore old session.
        """

        connection = event.data["connection"]

        username = event.data["username"]


        session = self._session_manager.get_by_username(
            username
        )


        if session is None:
            return



        session.reconnect(
            connection
        )


        self._session_manager.add_session(
            session
        )


        self._bus.publish(

            Event(

                EventType.SESSION_RECONNECTED,

                {
                    "session": session,

                    "username": username

                }

            )

        )