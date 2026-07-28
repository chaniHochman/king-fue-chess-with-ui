from server.bus.event import Event
from server.bus.event_type import EventType


class MatchmakingService:
    """
    Finds opponents for players.

    Responsible for:
    - storing waiting players
    - comparing ratings
    - creating matches

    Does not know:
    - rooms
    - games
    - networking
    - database
    """


    # Initialize matchmaking service.
    def __init__(
        self,
        bus
    ):
        """
        Store message bus.
        """

        self._bus = bus

        self._waiting_players = []

        self.register_events()



    # Register matchmaking events.
    def register_events(self):
        """
        Subscribe to match requests.
        """

        self._bus.subscribe(
            EventType.MATCH_REQUEST,
            self.handle_match_request
        )



    # Handle new match request.
    def handle_match_request(
        self,
        event
    ):
        """
        Add player and search opponent.
        """

        player = {
            "session":
            event.data["session"],

            "rating":
            event.data["rating"].user.rating
        }


        opponent = self.find_opponent(
            player
        )


        if opponent is None:

            self._waiting_players.append(
                player
            )

            return



        self._waiting_players.remove(
            opponent
        )


        self._bus.publish(
            Event(
                EventType.MATCH_FOUND,
                {
                    "player1":
                    opponent["session"],

                    "player2":
                    player["session"]
                }
            )
        )



    # Find suitable opponent.
    def find_opponent(
        self,
        player
    ):
        """
        Search player with close rating.
        """

        for waiting in self._waiting_players:

            difference = abs(
                waiting["rating"]
                -
                player["rating"]
            )


            if difference <= 100:

                return waiting


        return None