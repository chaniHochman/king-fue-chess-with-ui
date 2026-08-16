import time

from server.bus.event import Event
from server.bus.event_type import EventType
from server.config import ServerConfig



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

            EventType.MATCH_RESOLVED,
            self.add_player

        )



    # Add player to queue.
    def add_player(
        self,
        event
    ):
        """
        Handle MATCH_RESOLVED event.
        """

        session = event.data.get("session")
        rating = session.user.rating if session and session.user else 1200
        
        print(f"DEBUG MATCHMAKING: add_player called with session id={id(session)} username={session.username() if session else 'None'} rating={rating}")
        print(f"DEBUG MATCHMAKING: _queue size before: {len(self._queue)}")

        for waiting in self._queue:

            print(f"DEBUG MATCHMAKING: Checking waiting session id={id(waiting['session'])} username={waiting['session'].username()}")

            if abs(
                waiting["rating"] - rating
            ) <= 100:


                self._queue.remove(
                    waiting
                )


                print(f"DEBUG MATCHMAKING: MATCH FOUND! player1 id={id(waiting['session'])} username={waiting['session'].username()} player2 id={id(session)} username={session.username()}")
                
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