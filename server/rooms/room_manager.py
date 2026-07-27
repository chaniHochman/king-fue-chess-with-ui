# מנהל את כל החדרים בשרת.
# אחראי על:
# יצירת חדר חדש.
# שמירת חדרים פעילים.
# חיפוש חדר לפי room_id.
# הכנסת שחקנים לחדר.
# מחיקת חדר ריק.
# פרסום אירועים דרך MessageBus.

from server.rooms.room import Room


class RoomManager:
    """
    Stores and manages all active rooms.

    Responsible only for:
    - creating rooms
    - storing rooms
    - finding rooms
    - adding sessions
    - removing sessions
    - removing empty rooms

    Does not know:
    - MessageBus
    - networking
    - authentication
    - matchmaking
    - games
    """

    # Initialize room storage.
    def __init__(self):
        """
        Create an empty room collection.
        """

        self._rooms = {}

    # Create and store a new room.
    def create_room(self):
        """
        Create a new room object
        and store it by its id.
        """

        room = Room()

        self._rooms[room.room_id] = room

        return room

    # Find room by identifier.
    def get_room(
        self,
        room_id
    ):
        """
        Return a room by its id.

        Returns None if room does not exist.
        """

        return self._rooms.get(
            room_id
        )

    # Return all active rooms.
    def get_all_rooms(self):
        """
        Return a list of all active rooms.
        """

        return list(
            self._rooms.values()
        )

    # Add session into a room.
    def join_room(
        self,
        room_id,
        session
    ):
        """
        Add a session into an existing room.

        Returns the assigned role.
        """

        room = self.get_room(
            room_id
        )

        if room is None:
            return None

        return room.add_session(
            session
        )

    # Remove session from a room.
    def leave_room(
        self,
        room_id,
        session
    ):
        """
        Remove a session from a room.

        Deletes the room if it becomes empty.
        """

        room = self.get_room(
            room_id
        )

        if room is None:
            return

        room.remove_session(
            session
        )

        self.remove_empty_room(
            room
        )

    # Remove empty room.
    def remove_empty_room(
        self,
        room
    ):
        """
        Remove a room when no players
        or viewers remain inside.
        """

        if (
            room.white_player is not None
            or room.black_player is not None
            or len(room.viewers) > 0
        ):
            return

        self._rooms.pop(
            room.room_id,
            None
        )

    # Check if room is ready.
    def is_room_ready(
        self,
        room_id
    ):
        """
        Return True when the room
        has enough players to start a game.
        """

        room = self.get_room(
            room_id
        )

        if room is None:
            return False

        return room.is_ready()