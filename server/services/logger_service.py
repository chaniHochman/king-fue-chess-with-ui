#רושמת אירועים ללוג
from datetime import datetime
from server.bus.event_type import EventType


class LoggerService:
    """
    Logs important server events.

    Responsible only for:
    - receiving events
    - writing log file

    Does not know:
    - networking
    - rooms
    - games
    """

    # Create logger service.
    def __init__(self,bus):

        self.bus=bus
        self.file_name="logs/server.log"

        self.register_events()

    # Subscribe to server events.
    def register_events(self):
        """
        Register all events that should be logged.
        """

        events=[
            EventType.PLAYER_CONNECTED,
            EventType.PLAYER_DISCONNECTED,
            EventType.LOGIN_SUCCESS,
            EventType.LOGIN_FAILED,
            EventType.ROOM_CREATED,
            EventType.PLAYER_JOINED_ROOM,
            EventType.PLAYER_LEFT_ROOM,
            EventType.GAME_STARTED,
            EventType.GAME_FINISHED,
            EventType.MOVE_ACCEPTED,
            EventType.MOVE_REJECTED
        ]

        for event_type in events:
            self.bus.subscribe(
                event_type,
                self.write_log
            )

    # Write one event into the log file.
    def write_log(self,event):
        """
        Save one event into the server log.
        """

        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        text=(
            f"{timestamp} | "
            f"{event.type.value} | "
            f"{event.data}\n"
        )

        with open(
            self.file_name,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(text)