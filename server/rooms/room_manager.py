# מנהל את כל החדרים בשרת.
# אחראי על:
# יצירת חדר חדש.
# שמירת חדרים פעילים.
# חיפוש חדר לפי room_id.
# הכנסת שחקנים לחדר.
# מחיקת חדר ריק.
# פרסום אירועים דרך MessageBus.


from server.rooms.room import Room

from server.bus.event import Event

from server.bus.event_type import EventType



class RoomManager:
    """
    Manages all active game rooms.

    Responsible for:
    - creating rooms
    - finding rooms
    - joining rooms
    - removing empty rooms

    Communicates only through MessageBus.
    """



    # Initialize room manager.
    def __init__(
        self,
        bus
    ):
        """
        Initialize room storage
        and register event listeners.
        """

        self.bus = bus

        self.rooms = {}

        self.register_events()



    # Register room event handlers.
    def register_events(self):
        """
        Subscribe room requests
        to MessageBus.
        """

        self.bus.subscribe(
            EventType.CREATE_ROOM_REQUEST,
            self.handle_create_room
        )


        self.bus.subscribe(
            EventType.JOIN_ROOM_COMMAND,
            self.handle_join_room
        )



    # Handle create room request event.
    def handle_create_room(
        self,
        event
    ):
        """
        Create a new room after
        receiving request from client.
        """

        connection = event.data["connection"]


        room = self.create_room()


        self.bus.publish(
            Event(
                EventType.ROOM_CREATED,
                {
                    "connection": connection,
                    "room_id": room.room_id
                }
            )
        )



    # Handle join room request event.
    def handle_join_room(
        self,
        event
    ):
        """
        Join existing room after
        receiving request from client.
        """

        connection = event.data["connection"]

        room_id = event.data["room_id"]


        session = event.data.get(
            "session"
        )


        if session is None:
            return



        role = self.join_room(
            room_id,
            session
        )


        if role is None:

            self.bus.publish(
                Event(
                    EventType.ROOM_JOIN_FAILED,
                    {
                        "connection": connection,
                        "reason": "room_not_found"
                    }
                )
            )



    # Create a new game room.
    def create_room(
        self
    ):
        """
        Create and store a new room.
        """

        room = Room()


        self.rooms[
            room.room_id
        ] = room



        self.bus.publish(
            Event(
                EventType.ROOM_CREATED,
                {
                    "room_id":
                    room.room_id
                }
            )
        )


        return room



    # Find room by room id.
    def get_room(
        self,
        room_id
    ):
        """
        Return room by identifier.
        """

        return self.rooms.get(
            room_id
        )



    # Add player session into existing room.
    def join_room(
        self,
        room_id,
        session
    ):
        """
        Add session into room
        and assign role.
        """

        room = self.get_room(
            room_id
        )


        if room is None:

            return None



        role = room.add_session(
            session
        )
        # Check if two players are ready.
        if room.is_ready():

            self.start_game(room)


        self.bus.publish(
            Event(
                EventType.PLAYER_JOINED_ROOM,
                {
                    "room_id": room_id,

                    "username":
                    session.user.username,

                    "role": role
                }
            )
        )


        return role



    # Remove player from room.
    def leave_room(
        self,
        room_id,
        session
    ):
        """
        Remove session from room.
        """

        room = self.get_room(
            room_id
        )


        if room is None:

            return



        room.remove_session(
            session
        )


        self.bus.publish(
            Event(
                EventType.PLAYER_LEFT_ROOM,
                {
                    "room_id": room_id,

                    "username":
                    session.user.username
                }
            )
        )


        self.remove_empty_room(
            room
        )



    # Delete room if no users exist.
    def remove_empty_room(
        self,
        room
    ):
        """
        Remove room when nobody is inside.
        """

        if (
            room.white_player is None
            and
            room.black_player is None
            and
            len(room.viewers) == 0
        ):


            del self.rooms[
                room.room_id
            ]


            self.bus.publish(
                Event(
                    EventType.ROOM_REMOVED,
                    {
                        "room_id":
                        room.room_id
                    }
                )
            )



    # Return all active rooms.
    def get_all_rooms(
        self
    ):
        """
        Return list of active rooms.
        """

        return list(
            self.rooms.values()
        )
    # Start game when two players joined.
    def start_game(
        self,
        room
    ):

        self.bus.publish(
            Event(
                EventType.GAME_STARTED,
                {
                    "room_id":
                    room.room_id,

                    "white":
                    room.white_player,

                    "black":
                    room.black_player
                }
            )
        )