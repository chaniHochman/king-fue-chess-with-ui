# לקבל:

# connection

# ולהחזיר:

# Session

from server.bus.event import Event
from server.bus.event_type import EventType



class SessionResolver:
    """
    Finds connected user session.

    Responsible only for:
    - converting connection into session

    Does not know:
    - authentication
    - rooms
    - games
    """



    # Initialize session resolver.
    def __init__(
        self,
        bus,
        session_manager
    ):
        """
        Store references
        and subscribe to requests.
        """

        self.bus = bus

        self.session_manager = session_manager

        self.register_events()



    # Register events.
    def register_events(self):
        """
        Listen to room requests.
        """

        self.bus.subscribe(
            EventType.JOIN_ROOM_REQUEST,
            self.resolve_join_room
        )



    # Find session before joining room.
    def resolve_join_room(
        self,
        event
    ):
        """
        Add session object
        into room request.
        """

        connection = event.data["connection"]

        room_id = event.data["room_id"]

        session = self.find_session(
            connection
        )

        if session is None:

            return



        self.bus.publish(
            Event(
                EventType.JOIN_ROOM_REQUEST,
                {
                    "connection": connection,

                    "room_id": room_id,

                    "session": session
                }
            )
        )

    # Find session by connection.
    def find_session(
        self,
        connection
    ):
        """
        Search active sessions.
        """


        sessions = (
            self.session_manager
            .get_all_sessions()
        )

        for session in sessions:

            if session.connected == connection:

                return session

        return None