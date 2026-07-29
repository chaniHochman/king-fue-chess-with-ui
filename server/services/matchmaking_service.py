import time

from server.bus.event import Event
from server.bus.event_type import EventType
from server.config.server_config import ServerConfig



class MatchmakingService:
    """
    Finds opponents.

    Responsible for:
    - matchmaking queue
    - rating comparison
    - timeout handling

    Does not know:
    - game rules
    - rooms
    """



    # Initialize matchmaking.
    def __init__(
        self,
        bus
    ):
        """
        Store dependencies.
        """

        self._bus = bus


        self._queue = []


        self.register_events()



    # Register events.
    def register_events(
        self
    ):
        """
        Listen for matchmaking requests.
        """

        self._bus.subscribe(

            EventType.MATCH_REQUEST,

            self.add_player

        )



    # Add player to queue.
    def add_player(
        self,
        event
    ):
        """
        Search opponent.
        """

        session = event.data["session"]



        rating = session.user.rating



        for waiting in self._queue:


            if abs(
                waiting["rating"] - rating
            ) <= 100:


                self._queue.remove(
                    waiting
                )


                self._bus.publish(

                    Event(

                        EventType.MATCH_FOUND,

                        {
                            "player1":
                            waiting["session"],

                            "player2":
                            session

                        }

                    )

                )


                return



        self._queue.append(

            {
                "session": session,

                "rating": rating,

                "time": time.time()

            }

        )



    # Remove expired searches.
    def cleanup(
        self
    ):
        """
        Remove players waiting too long.
        """

        now = time.time()


        expired = []


        for item in self._queue:


            if now - item["time"] >= ServerConfig.MATCHMAKING_TIMEOUT:


                expired.append(
                    item
                )


        for item in expired:


            self._queue.remove(
                item
            )


            self._bus.publish(

                Event(

                    EventType.MATCH_FAILED,

                    {
                        "session":
                        item["session"]

                    }

                )

            )