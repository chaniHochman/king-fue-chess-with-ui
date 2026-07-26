#אחראית רק על משחק אחד
from server.bus.event import Event
from server.bus.event_type import EventType



class GameSession:
    """
    Represents one active game session.

    Responsible for:
    - connecting players to a game
    - forwarding moves
    - storing game state

    Does not know:
    - networking
    - database
    - authentication
    """



    # Create new game session.
    def __init__(
        self,
        room,
        server_game,
        bus
    ):
        """
        Initialize game session.
        """

        self.room = room

        self.server_game = server_game

        self.bus = bus

        self.finished = False



    # Handle player move.
    def make_move(
        self,
        move,
        player=None
    ):
        """
        Forward move to game engine.
        """


        if self.finished:

            return None



        result = (
            self.server_game
            .make_move(move)
        )



        if result.success:

            self.bus.publish(

                Event(

                    EventType.MOVE_ACCEPTED,

                    {
                        "room_id":
                        self.room.room_id,


                        "move":
                        move

                    }

                )

            )

        else:

            self.bus.publish(

                Event(

                    EventType.MOVE_REJECTED,

                    {
                        "move":
                        move
                    }

                )

            )


        return result

    # Finish game.
    def finish(
        self
    ):
        """
        Mark game as finished.
        """

        self.finished = True

            # Return current game snapshot.
    def get_snapshot(
        self
    ):
        """
        Return current state
        of the running game.
        """

        return self.server_game.get_snapshot()