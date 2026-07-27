#מחזיקה את כל סוגי ההודעות האפשריים.
from enum import Enum


class MessageType(Enum):
    """
    Defines all network messages.
    """


    LOGIN = "LOGIN"

    REGISTER = "REGISTER"


    PLAY = "PLAY"


    CREATE_ROOM = "CREATE_ROOM"

    JOIN_ROOM = "JOIN_ROOM"

    CANCEL_ROOM = "CANCEL_ROOM"


    MOVE = "MOVE"


    RECONNECT = "RECONNECT"


    GAME_STATE = "GAME_STATE"

    GAME_STARTED = "GAME_STARTED"

    GAME_ENDED = "GAME_ENDED"


    ERROR = "ERROR"

    SCORE_UPDATE = "SCORE_UPDATE"