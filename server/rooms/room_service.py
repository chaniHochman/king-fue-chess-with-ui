from server.bus.event import Event
from server.bus.event_type import EventType


class RoomService:
    """
    Handles room related events.

    Responsible for:
    - creating rooms
    - joining rooms
    - notifying room changes

    Uses:
    - MessageBus
    - RoomManager

    Does not know:
    - network
    - database
    - authentication
    - game logic
    """


    # Initialize room service.
    def __init__(
        self,
        bus,
        room_manager
    ):
        """
        Store dependencies
        and register event listeners.
        """

        self._bus = bus

        self._room_manager = room_manager

        self.register_events()



    # Register room event handlers.
    def register_events(self):
        """
        Subscribe to room requests.
        """

        self._bus.subscribe(
            EventType.CREATE_ROOM_REQUEST,
            self.create_room
        )


        self._bus.subscribe(
            EventType.JOIN_ROOM_REQUEST,
            self.join_room
        )



    # Handle create room request.
    def create_room(
        self,
        event
    ):
        """
        Create a new room.

        Uses RoomManager only.
        """

        connection = event.data["connection"]

        session = event.data.get(
            "session"
        )


        room = self._room_manager.create_room()


        if session is not None:

            self._room_manager.join_room(
                room.room_id,
                session
            )


        self._bus.publish(

            Event(

                EventType.ROOM_CREATED,

                {
                    "connection": connection,

                    "room_id":
                    room.room_id
                }

            )

        )



    # Handle join room request.
    def join_room(
        self,
        event
    ):
        """
        Add player or viewer into room.
        """

        connection = event.data["connection"]

        room_id = event.data["room_id"]

        session = event.data.get(
            "session"
        )


        if session is None:

            return



        role = self._room_manager.join_room(
            room_id,
            session
        )


        if role is None:

            self._bus.publish(

                Event(

                    EventType.ROOM_JOIN_FAILED,

                    {
                        "connection": connection,

                        "reason":
                        "room_not_found"
                    }

                )

            )

            return



        self._bus.publish(

            Event(

                EventType.PLAYER_JOINED_ROOM,

                {
                    "room_id":
                    room_id,

                    "username":
                    session.user.username,

                    "role":
                    role
                }

            )

        )


        if self._room_manager.is_room_ready(room_id):

            room = self._room_manager.get_room(
                room_id
            )


            self._bus.publish(

                Event(

                    EventType.GAME_STARTED,

                    {
                        "room_id":
                        room_id,

                        "white":
                        room.white_player,

                        "black":
                        room.black_player
                    }

                )

            )