from server.session.session import Session
from server.bus.event import Event
from server.bus.event_type import EventType


class SessionService:
    """
    Creates user sessions after login.

    Responsible for:
    - creating Session objects
    - storing sessions

    Does not know:
    - authentication logic
    - rooms
    - games
    - database
    """



    # Initialize session service.
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



    # Register event listeners.
    def register_events(
        self
    ):
        """
        Listen to login success.
        """

        self._bus.subscribe(
            EventType.LOGIN_SUCCESS,
            self.create_session
        )



    # Create session after login.
    def create_session(
        self,
        event
    ):
        """
        Create online session
        after successful authentication.
        """


        user = event.data["user"]

        connection = event.data["connection"]


        session = Session(
            connection,
            user
        )


        self._session_manager.add_session(
            session
        )


        self._bus.publish(

            Event(

                EventType.SESSION_CREATED,

                {
                    "session": session,

                    "username":
                    user.username

                }

            )

        )