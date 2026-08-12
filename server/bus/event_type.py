from enum import Enum


class EventType(Enum):
    """
    All internal server events.

    Events are exchanged through MessageBus.

    Components communicate only through events.
    """


    # Network events
    CLIENT_MESSAGE = "client_message"
    CLIENT_CONNECTED = "client_connected"
    CLIENT_DISCONNECTED = "client_disconnected"


    # Authentication events
    LOGIN_REQUEST = "login_request"
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"

    REGISTER_REQUEST = "register_request"
    REGISTER_SUCCESS = "register_success"
    REGISTER_FAILED = "register_failed"



    # Session events
    SESSION_CREATED = "session_created"
    SESSION_DISCONNECTED = "session_disconnected"

    RECONNECT_REQUEST = "reconnect_request"
    RECONNECT_SUCCESS = "reconnect_success"



    # Room events
    CREATE_ROOM_REQUEST = "create_room_request"
    ROOM_CREATED = "room_created"

    JOIN_ROOM_REQUEST = "join_room_request"
    PLAYER_JOINED_ROOM = "player_joined_room"

    LEAVE_ROOM_REQUEST = "leave_room_request"
    PLAYER_LEFT_ROOM = "player_left_room"

    ROOM_REMOVED = "room_removed"


    # Matchmaking events
    MATCH_REQUEST = "match_request"
    MATCH_FOUND = "match_found"
    MATCH_FAILED = "match_failed"



    # Game events
    GAME_CREATED = "game_created"
    GAME_STARTED = "game_started"

    MOVE_REQUESTED = "move_requested"
    MOVE_ACCEPTED = "move_accepted"
    MOVE_REJECTED = "move_rejected"

    GAME_STATE_UPDATED = "game_state_updated"

    GAME_ENDED = "game_ended"



    # Services
    SCORE_UPDATED = "score_updated"

    SOUND_EVENT = "sound_event"

    ANIMATION_EVENT = "animation_event"

    LOG_EVENT = "log_event"

    SESSION_RECONNECTED="session_reconnected"

    START_GAME="start_game"

    GAME_FINISHED="game_finished"

    PLAYER_TIMEOUT="player_timeout"

    DISCONNECT_TIMEOUT = "disconnect_timeout"


    # Response events
    ROOM_JOIN_FAILED = "room_join_failed"

    GAME_STATE_CHANGED = "game_state_changed"

    PLAY_SOUND = "play_sound"

    PLAY_ANIMATION = "play_animation"

    ROOM_CREATE_RESOLVED = "room_create_resolved"

    MATCH_RESOLVED = "match_resolved"