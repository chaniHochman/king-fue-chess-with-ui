import time
import threading

from server.bus.event import Event
from server.bus.event_type import EventType


class DisconnectMonitor:
    """
    Monitors disconnected players.

    Responsible for:
    - starting disconnect timers
    - checking reconnect timeout
    - publishing timeout events

    Does not know:
    - games
    - rooms
    - database
    - networking
    """

    TIMEOUT_SECONDS = 20


    # Initialize disconnect monitor.
    def __init__(
        self,
        bus,
        session_manager
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._session_manager = session_manager

        self._timers = {}

        self.register_events()



    # Register disconnect events.
    def register_events(self):
        """
        Subscribe to disconnect notifications.
        """

        self._bus.subscribe(
            EventType.PLAYER_DISCONNECTED,
            self.handle_disconnect
        )



    # Start timeout timer.
    def handle_disconnect(
        self,
        event
    ):
        """
        Start timer after disconnect.
        """

        session = event.data.get(
            "session"
        )

        if session is None:
            return


        username = session.user.username


        timer = threading.Timer(
            self.TIMEOUT_SECONDS,
            self.check_timeout,
            args=(username,)
        )


        self._timers[username] = timer

        timer.start()



    # Check if player returned.
    def check_timeout(
        self,
        username
    ):
        """
        Publish timeout if player did not reconnect.
        """

        session = self._session_manager.get_session(
            username
        )


        if session is None:
            return


        if session.is_connected():
            return



        self._bus.publish(
            Event(
                EventType.PLAYER_TIMEOUT,
                {
                    "username":
                    username,

                    "session":
                    session
                }
            )
        )


        self._timers.pop(
            username,
            None
        )



    # Cancel timeout after reconnect.
    def cancel_timer(
        self,
        username
    ):
        """
        Stop disconnect timer.
        """

        timer = self._timers.get(
            username
        )


        if timer:

            timer.cancel()


        self._timers.pop(
            username,
            None
        )