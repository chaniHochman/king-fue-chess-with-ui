import uuid



class RoomManager:
    """
    Stores all rooms.

    Responsible for:
    - creating rooms
    - finding rooms
    - removing rooms

    Does not know:
    - games
    - users
    """



    # Initialize manager.
    def __init__(
        self
    ):
        """
        Create room storage.
        """

        self._rooms = {}



    # Create room.
    def create_room(
        self
    ):
        """
        Create unique room id.
        """

        room_id = str(
            uuid.uuid4()
        )[:8]


        from server.rooms.room import Room


        room = Room(
            room_id
        )


        self._rooms[room_id] = room


        return room



    # Find room.
    def get_room(
        self,
        room_id
    ):
        """
        Return room.
        """

        return self._rooms.get(
            room_id
        )



    # Remove room.
    def remove_room(
        self,
        room_id
    ):
        """
        Delete room.
        """

        return self._rooms.pop(
            room_id,
            None
        )



    # Find room by game id.
    def get_room_by_game_id(
        self,
        game_id
    ):
        """
        Return room with matching game_id.
        """

        for room in self._rooms.values():

            if room.game_id == game_id:

                return room

        return None



    # Return all rooms.
    def get_all_rooms(
        self
    ):
        """
        Return rooms list.
        """

        return list(
            self._rooms.values()
        )