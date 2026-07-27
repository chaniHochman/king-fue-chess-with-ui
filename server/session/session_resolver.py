from server.bus.event import Event
from server.bus.event_type import EventType


class SessionResolver:
    """
    Resolves client connection into user session.

    Responsible only for:
    - finding Session by connection
    - forwarding events with session attached

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
        Store dependencies
        and register listeners.
        """

        self._bus = bus
        self._session_manager = session_manager

        self.register_events()


    # Register events.
    def register_events(self):
        """
        Subscribe to events
        that require a Session.
        """

        self._bus.subscribe(
            EventType.CREATE_ROOM_REQUEST,
            self.resolve_create_room
        )

        self._bus.subscribe(
            EventType.JOIN_ROOM_REQUEST,
            self.join_room
        )

        self._bus.subscribe(
            EventType.MOVE_REQUESTED,
            self.resolve_move
        )

        self._bus.subscribe(
            EventType.MATCH_REQUEST,
            self.resolve_match
        )


    # Resolve create room request.
    def resolve_create_room(
        self,
        event
    ):
        """
        Add Session to create room event.
        """

        self.forward_event(
            EventType.CREATE_ROOM_REQUEST,
            event
        )


    # Resolve join room request.
    def resolve_join_room(
        self,
        event
    ):
        """
        Add Session to join room event.
        """

        self.forward_event(
            EventType.JOIN_ROOM_REQUEST,
            event
        )


    # Resolve move request.
    def resolve_move(
        self,
        event
    ):
        """
        Add Session to move event.
        """

        self.forward_event(
            EventType.MOVE_REQUESTED,
            event
        )


    # Resolve matchmaking request.
    def resolve_match(
        self,
        event
    ):
        """
        Add Session to matchmaking event.
        """

        self.forward_event(
            EventType.MATCH_REQUEST,
            event
        )


    # Find session and publish updated event.
    def forward_event(
        self,
        event_type,
        event
    ):
        """
        Find session from connection
        and publish new event.
        """

        connection = event.data["connection"]

        session = self.find_session(
            connection
        )

        if session is None:
            return


        data = event.data.copy()

        data["session"] = session

        event.resolved = True
        
        self._bus.publish(
            Event(
                event_type,
                data
            )
        )


    # Find session by connection.
    def find_session(
        self,
        connection
    ):
        """
        Search SessionManager
        for matching connection.
        """

        return self._session_manager.get_by_connection(
            connection
        )