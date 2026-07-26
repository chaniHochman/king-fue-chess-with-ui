from enum import Enum


class EventType(Enum):
    """
    Defines all server events.
    """

    CLIENT_MESSAGE = "client_message"
    PLAYER_CONNECTED = "player_connected"
    PLAYER_DISCONNECTED = "player_disconnected"

    LOGIN_REQUEST = "login_request"
    REGISTER_REQUEST = "register_request"
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    REGISTER_FAILED = "register_failed"

    CREATE_ROOM_REQUEST = "create_room_request"
    JOIN_ROOM_REQUEST = "join_room_request"
    JOIN_ROOM_COMMAND = "join_room_command"
    ROOM_CREATED = "room_created"
    PLAYER_JOINED_ROOM = "player_joined_room"
    PLAYER_LEFT_ROOM = "player_left_room"
    ROOM_JOIN_FAILED = "room_join_failed"
    ROOM_REMOVED = "room_removed"

    GAME_STARTED = "game_started"
    GAME_FINISHED = "game_finished"

    MOVE_REQUESTED = "move_requested"
    MOVE_ACCEPTED = "move_accepted"
    MOVE_REJECTED = "move_rejected"

    MATCH_REQUEST = "match_request"
    PLAY_ANIMATION = "play_animation"
    PLAY_SOUND = "play_sound"