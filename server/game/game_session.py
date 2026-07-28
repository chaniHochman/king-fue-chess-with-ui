from server.bus.event import Event
from server.bus.event_type import EventType


class GameSession:
    """
    Represents one active multiplayer match.

    Responsible for:
    - connecting room to server game
    - providing game state
    - finishing game

    Does not know:
    - networking
    - database
    - authentication
    - game rules
    """



    # Initialize game session.
    def __init__(
        self,
        room,
        server_game,
        bus
    ):
        """
        Store game objects.
        """

        self.room = room

        self.server_game = server_game

        self._bus = bus

        self.finished = False



    # Execute player move.
    def make_move(
        self,
        move
    ):
        """
        Forward move
        to ServerGame.
        """

        if self.finished:

            return None


        return self.server_game.make_move(
            move
        )



    # Return current game snapshot.
    def get_snapshot(
        self
    ):
        """
        Return current state
        from game engine.
        """

        if self.finished:

            return None


        return self.server_game.get_snapshot()



    # Finish current game.
    def finish(
        self,
        winner=None,
        loser=None,
        reason="unknown"
    ):
        """
        Mark game as finished
        and notify services.
        """

        if self.finished:

            return


        self.finished = True


        self._bus.publish(

            Event(

                EventType.GAME_FINISHED,

                {
                    "room_id":
                    self.room.room_id,

                    "winner":
                    winner,

                    "loser":
                    loser,

                    "reason":
                    reason
                }

            )

        )



    # Check if game finished.
    def is_finished(
        self
    ):
        """
        Return game status.
        """

        return self.finished



    # Return room.
    def get_room(
        self
    ):
        """
        Return related room.
        """

        return self.room