import time

from server.bus.event import Event
from server.bus.event_type import EventType


class DisconnectMonitor:
    """
    Monitors disconnected players.

    Responsible for:
    - checking disconnect timeout
    - publishing player timeout

    Does not know:
    - networking
    - games
    - database
    """



    # Initialize disconnect monitor.
    def __init__(
        self,
        bus,
        session_manager,
        timeout_seconds=20
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._session_manager = session_manager

        self._timeout = timeout_seconds

        self.register_events()



    # Register disconnect events.
    def register_events(
        self
    ):
        """
        Listen to disconnect events.
        """

        self._bus.subscribe(
            EventType.SESSION_DISCONNECTED,
            self.check_sessions
        )



    # Check disconnected sessions.
    def check_sessions(
        self,
        event=None
    ):
        """
        Find sessions that passed timeout.
        """

        now = time.time()


        for session in self._session_manager.get_all_sessions():

            if session.connected:
                continue


            if session.disconnect_time is None:

                session.disconnect_time = now

                continue


            elapsed = now - session.disconnect_time


            if elapsed >= self._timeout:

                self._bus.publish(
                    Event(
                        EventType.PLAYER_TIMEOUT,
                        {
                            "session": session
                        }
                    )
                )