from server.bus.event import Event
from server.bus.event_type import EventType



class SessionResolver:
    """
    Attaches Session object
    to user related events.

    Responsible for:
    - finding session
    - enriching events

    Does not know:
    - rooms
    - games
    - authentication
    """



    # Initialize resolver.
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



    # Register listeners.
    def register_events(
        self
    ):
        """
        Listen to events
        requiring sessions.
        """


        self._bus.subscribe(
            EventType.CREATE_ROOM_REQUEST,
            self.resolve_create_room
        )


        self._bus.subscribe(
            EventType.JOIN_ROOM_REQUEST,
            self.resolve_join_room
        )


        self._bus.subscribe(
            EventType.MOVE_REQUESTED,
            self.resolve_move
        )


        self._bus.subscribe(
            EventType.MATCH_REQUEST,
            self.resolve_match
        )



    # Resolve create room.
    def resolve_create_room(
        self,
        event
    ):
        self.forward_event(
            EventType.ROOM_CREATE_RESOLVED,
            event
        )



    # Resolve join room.
    def resolve_join_room(
        self,
        event
    ):
        self.forward_event(
            EventType.JOIN_ROOM_REQUEST,
            event
        )



    # Resolve move.
    def resolve_move(
        self,
        event
    ):
        self.forward_event(
            EventType.MOVE_REQUESTED,
            event
        )



    # Resolve matchmaking.
    def resolve_match(
        self,
        event
    ):
        self.forward_event(
            EventType.MATCH_RESOLVED,
            event
        )



    # Attach session.
    def forward_event(
        self,
        event_type,
        event
    ):
        """
        Add Session information
        and publish new event.
        """


        if getattr(
            event,
            "resolved",
            False
        ):
            return



        connection = event.data["connection"]


        session = self.find_session(
            connection
        )


        if session is None:
            return



        data = event.data.copy()


        data["session"] = session


        new_event = Event(
            event_type,
            data
        )


        new_event.resolved = True


        self._bus.publish(
            new_event
        )



    # Find session.
    def find_session(
        self,
        connection
    ):
        """
        Search session manager.
        """

        return self._session_manager.get_by_connection(
            connection
        )



    # Compatibility method.
    def get_session(
        self,
        connection
    ):
        return self.find_session(
            connection
        )