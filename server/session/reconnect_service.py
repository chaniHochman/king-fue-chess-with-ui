#התחברות מחדש
from server.bus.event import Event
from server.bus.event_type import EventType


class ReconnectService:
    """
    Handles reconnect requests.

    Responsible only for:
    - finding old sessions
    - attaching new connections

    Does not know:
    - games
    - rooms
    - database
    """


    # Initialize reconnect service.
    def __init__(
        self,
        bus,
        session_manager
    ):
        """
        Store dependencies
        and register listeners.
        """

        self._bus = bus

        self._session_manager = session_manager

        self.register_events()



    # Register reconnect events.
    def register_events(self):
        """
        Subscribe to reconnect requests.
        """

        self._bus.subscribe(

            EventType.RECONNECT_REQUEST,

            self.handle_reconnect

        )



    # Handle reconnect request.
    def handle_reconnect(
        self,
        event
    ):
        """
        Try to reconnect existing session.
        """

        connection = event.data["connection"]

        username = event.data["username"]


        session = self._session_manager.get_session(
            username
        )


        if session is None:

            return



        if not session.can_reconnect():

            return



        session.reconnect(
            connection
        )


        self._bus.publish(

            Event(

                EventType.SESSION_CREATED,

                {
                    "session": session,

                    "username": username

                }

            )

        )