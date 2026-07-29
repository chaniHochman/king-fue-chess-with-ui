from enum import Enum


class MessageType(Enum):

    LOGIN = "login"
    REGISTER = "register"

    PLAY = "play"

    CREATE_ROOM = "create_room"
    JOIN_ROOM = "join_room"
    LEAVE_ROOM = "leave_room"

    MOVE = "move"

    GAME_STATE = "game_state"

    CHAT = "chat"

    ERROR = "error"

    LOGIN_SUCCESS = "login_success"

    GAME_STARTED = "game_started"

    GAME_ENDED = "game_ended"

    SCORE_UPDATE = "score_update"

    PLAY_SOUND = "play_sound"

    PLAY_ANIMATION = "play_animation"