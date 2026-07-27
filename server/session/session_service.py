# להאזין ל־LOGIN_SUCCESS
# ליצור Session
# לשמור אותו ב־SessionManager
from server.session.session import Session

from server.bus.event import Event

from server.bus.event_type import EventType


class SessionService:
    """
    Creates online sessions.

    Responsible only for:
    - creating Session objects
    - storing sessions

    Does not know:
    - authentication
    - rooms
    - games
    """


    # Initialize session service.
    def __init__(
        self,
        bus,
        session_manager
    ):
        """
        Store dependencies
        and register listeners.
        """

        self.bus = bus

        self.session_manager = session_manager

        self.register_events()



    # Register event listeners.
    def register_events(self):
        """
        Listen to successful login.
        """

        self.bus.subscribe(
            EventType.LOGIN_SUCCESS,
            self.create_session
        )



    # Create session after login.
    def create_session(
        self,
        event
    ):
        """
        Create a new online session
        and notify the server.
        """


        user = event.data["user"]

        connection = event.data["connection"]


        session = Session(
            user,
            connection
        )


        self.session_manager.add_session(
            session
        )


        self.bus.publish(

            Event(

                EventType.SESSION_CREATED,

                {
                    "session": session,

                    "username":
                    user.username
                }

            )

        )