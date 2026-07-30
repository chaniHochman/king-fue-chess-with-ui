from enum import Enum


class MessageType(Enum):

    LOGIN = "login"

    REGISTER = "register"


    PLAY = "play"


    CREATE_ROOM = "create_room"

    JOIN_ROOM = "join_room"

    LEAVE_ROOM = "leave_room"



    ROOM_CREATED = "room_created"

    ROOM_JOINED = "room_joined"



    MOVE = "move"


    GAME_STATE = "game_state"


    GAME_STARTED = "game_started"

    GAME_ENDED = "game_ended"



    SCORE_UPDATE = "score_update"



    ERROR = "error"



    LOGIN_SUCCESS = "login_success"

    REGISTER_SUCCESS = "register_success"



    PLAY_SOUND = "play_sound"

    PLAY_ANIMATION = "play_animation"



    CHAT = "chat"