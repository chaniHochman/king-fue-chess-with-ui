import threading
import time

from server.config import ServerConfig
from server.bus.event import Event
from server.bus.event_type import EventType



class DisconnectMonitor:
    """
    Monitors disconnected sessions.

    Responsible for:
    - checking disconnect timeout
    - publishing timeout events

    Does not know:
    - games
    - rooms
    - rating
    """



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

        self._running = False

        self._thread = None



    # Start monitoring thread.
    def start(
        self
    ):
        """
        Start background monitor.
        """

        self._running = True


        self._thread = threading.Thread(

            target=self.monitor_loop,

            daemon=True

        )


        self._thread.start()



    # Stop monitor.
    def stop(
        self
    ):
        """
        Stop background thread.
        """

        self._running = False



    # Main monitoring loop.
    def monitor_loop(
        self
    ):
        """
        Check disconnected users.
        """

        while self._running:


            sessions = self._session_manager.get_all_sessions()


            now = time.time()


            for session in sessions:


                if session.connected:

                    continue


                if session.disconnect_time is None:

                    continue



                elapsed = now - session.disconnect_time



                if elapsed >= ServerConfig.DISCONNECT_TIMEOUT:


                    self._bus.publish(

                        Event(

                            EventType.DISCONNECT_TIMEOUT,

                            {
                                "session": session
                            }

                        )

                    )

                    self._session_manager.remove_session(session.connection)



            time.sleep(1)