#מחזיקה את כל סוגי ההודעות האפשריים.
from enum import Enum


class MessageType(Enum):
    """
    Defines client-server commands.

    Used for communication
    between client and server.
    """

    LOGIN = "login"

    REGISTER = "register"

    PLAY = "play"

    CREATE_ROOM = "create_room"

    JOIN_ROOM = "join_room"

    LEAVE_ROOM = "leave_room"

    MOVE = "move"

    GAME_STATE = "game_state"

    CHAT = "chat"