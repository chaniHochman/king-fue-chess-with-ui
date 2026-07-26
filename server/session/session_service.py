# להאזין ל־LOGIN_SUCCESS
# ליצור Session
# לשמור אותו ב־SessionManager
from server.session.session import Session

from server.bus.event import Event

from server.bus.event_type import EventType



class SessionService:
    """
    Creates and manages online sessions.

    Responsible for:
    - creating Session objects
    - adding sessions to SessionManager

    Does not know:
    - authentication logic
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
        Initialize service
        and subscribe to events.
        """

        self.bus = bus

        self.session_manager = session_manager

        self.register_events()



    # Register session events.
    def register_events(self):
        """
        Subscribe to login success events.
        """

        self.bus.subscribe(
            EventType.LOGIN_SUCCESS,
            self.create_session
        )



    # Create new online session.
    def create_session(
        self,
        event
    ):
        """
        Create session after successful login.
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