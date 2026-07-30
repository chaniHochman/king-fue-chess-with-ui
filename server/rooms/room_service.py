from server.bus.event import Event
from server.bus.event_type import EventType



class RoomService:
    """
    Handles room events.

    Responsible for:
    - creating rooms
    - joining rooms

    Does not know:
    - games
    - authentication
    """



    # Initialize service.
    def __init__(
        self,
        bus,
        room_manager
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._room_manager = room_manager

        self.register_events()



    # Register listeners.
    def register_events(
        self
    ):
        """
        Subscribe to room events.
        """

        self._bus.subscribe(
            EventType.ROOM_CREATE_RESOLVED,
            self.create_room
        )


        self._bus.subscribe(
            EventType.JOIN_ROOM_REQUEST,
            self.join_room
        )



    # Create room.
    def create_room(
        self,
        event
    ):
        """
        Create new room.
        """
        if not event.resolved:
            return

        session = event.data["session"]


        room = self._room_manager.create_room()


        role = room.add_player(
            session
        )


        session.join_room(
            room
        )


        self._bus.publish(

            Event(

                EventType.ROOM_CREATED,

                {
                    "room": room,

                    "room_id": room.room_id,

                    "session": session,

                    "role": role
                }

            )

        )



    # Join room.
    def join_room(
        self,
        event
    ):
        """
        Join existing room.
        """
        if not event.resolved:
            return

        session = event.data["session"]

        room_id = event.data["room_id"]


        room = self._room_manager.get_room(
            room_id
        )


        if room is None:

            return



        role = room.add_player(
            session
        )


        session.join_room(
            room
        )


        self._bus.publish(

            Event(

                EventType.PLAYER_JOINED_ROOM,

                {
                    "room": room,

                    "session": session,

                    "role": role
                }

            )

        )