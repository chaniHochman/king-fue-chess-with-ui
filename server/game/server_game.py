from server.bus.event import Event
from server.bus.event_type import EventType


class ServerGame:
    """
    Represents one active game on server.

    Responsible for:
    - storing game engine
    - forwarding moves
    - publishing game events

    Does not know:
    - rooms
    - authentication
    - network
    """



    # Initialize server game.
    def __init__(
        self,
        game_id,
        game_engine,
        bus
    ):
        """
        Store game information.
        """

        self.game_id = game_id

        self.game_engine = game_engine

        self.bus = bus



        self.finished = False



    # Execute player move.
    def make_move(
        self,
        source,
        target
    ):
        """
        Send move request
        to authoritative GameEngine.
        """


        if self.finished:

            return False



        result = self.game_engine.request_move(
            source,
            target
        )


        if result.success:


            self.bus.publish(

                Event(

                    EventType.MOVE_ACCEPTED,

                    {
                        "game_id": self.game_id,

                        "source": source,

                        "target": target

                    }

                )

            )


        else:


            self.bus.publish(

                Event(

                    EventType.MOVE_REJECTED,

                    {
                        "game_id": self.game_id,

                        "reason": result.reason

                    }

                )

            )



        return result



    # Get current game state.
    def get_snapshot(
        self
    ):
        """
        Return current board snapshot.
        """

        return self.game_engine.create_snapshot()



    # Check if game ended.
    def is_finished(
        self
    ):
        """
        Return game status.
        """

        return self.finished



    # Finish game.
    def finish(
        self
    ):
        """
        Mark game as finished.
        """

        self.finished = True


        self.bus.publish(

            Event(

                EventType.GAME_ENDED,

                {
                    "game_id": self.game_id
                }

            )

        )