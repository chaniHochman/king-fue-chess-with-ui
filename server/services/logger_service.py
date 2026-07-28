#רושמת אירועים ללוג
from datetime import datetime

from server.bus.event_type import EventType


class LoggerService:
    """
    Stores server activity logs.

    Responsible for:
    - listening to server events
    - creating logs

    Does not know:
    - games
    - authentication
    - networking
    """


    # Initialize logger.
    def __init__(
        self,
        bus
    ):
        """
        Store bus and register events.
        """

        self._bus = bus

        self._logs = []

        self.register_events()



    # Register events to log.
    def register_events(self):
        """
        Subscribe to important events.
        """

        events = [

            EventType.LOGIN_SUCCESS,

            EventType.LOGIN_FAILED,

            EventType.ROOM_CREATED,

            EventType.PLAYER_JOINED_ROOM,

            EventType.PLAYER_LEFT_ROOM,

            EventType.GAME_STARTED,

            EventType.GAME_FINISHED,

            EventType.MOVE_ACCEPTED,

            EventType.MOVE_REJECTED,

            EventType.PLAYER_TIMEOUT

        ]


        for event_type in events:

            self._bus.subscribe(
                event_type,
                self.log_event
            )



    # Store event log.
    def log_event(
        self,
        event
    ):
        """
        Save event information.
        """

        log = {

            "time":
            datetime.now().isoformat(),

            "event":
            event.type.value,

            "data":
            event.data

        }


        self._logs.append(
            log
        )



    # Return logs.
    def get_logs(
        self
    ):
        """
        Return all logs.
        """

        return list(
            self._logs
        )