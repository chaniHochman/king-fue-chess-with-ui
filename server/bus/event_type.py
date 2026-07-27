from enum import Enum


class EventType(Enum):
    """
    Defines all internal server events.

    Every communication between
    server components uses this enum.
    """


    # Network events

    CLIENT_CONNECTED = "client_connected"

    CLIENT_DISCONNECTED = "client_disconnected"

    CLIENT_MESSAGE = "client_message"



    # Authentication events

    LOGIN_REQUEST = "login_request"

    REGISTER_REQUEST = "register_request"

    LOGIN_SUCCESS = "login_success"

    LOGIN_FAILED = "login_failed"

    REGISTER_SUCCESS = "register_success"

    REGISTER_FAILED = "register_failed"



    # Session events

    SESSION_CREATED = "session_created"

    SESSION_REMOVED = "session_removed"

    SESSION_RECONNECTED = "session_reconnected"



    # Room events

    CREATE_ROOM_REQUEST = "create_room_request"

    JOIN_ROOM_REQUEST = "join_room_request"

    LEAVE_ROOM_REQUEST = "leave_room_request"

    ROOM_CREATED = "room_created"

    PLAYER_JOINED_ROOM = "player_joined_room"

    PLAYER_LEFT_ROOM = "player_left_room"

    ROOM_JOIN_FAILED = "room_join_failed"

    ROOM_REMOVED = "room_removed"



    # Matchmaking events

    MATCH_REQUEST = "match_request"

    MATCH_FOUND = "match_found"

    MATCH_FAILED = "match_failed"



    # Game events

    GAME_CREATED = "game_created"

    GAME_STARTED = "game_started"

    GAME_FINISHED = "game_finished"

    GAME_STATE_CHANGED = "game_state_changed"



    # Move events

    MOVE_REQUESTED = "move_requested"

    MOVE_ACCEPTED = "move_accepted"

    MOVE_REJECTED = "move_rejected"



    # Player events

    PLAYER_TIMEOUT = "player_timeout"

    PLAYER_RESIGNED = "player_resigned"



    # Client effects

    PLAY_SOUND = "play_sound"

    PLAY_ANIMATION = "play_animation"



    # Rating

    SCORE_UPDATE_REQUEST = "score_update_request"

    SCORE_UPDATED = "score_updated"



    # Logging

    SERVER_LOG = "server_log"


    SESSION_CREATED = "session_created"

    RECONNECT_REQUEST = "reconnect_request"