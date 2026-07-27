# אחראית רק על משחק אחד
# באיזה Room המשחק נמצא.
# מי השחקן הלבן.
# מי השחקן השחור.
# מי הצופים.
# מהו ServerGame.
# האם המשחק הסתיים.
# להחזיר Snapshot.
# להעביר מהלכים ל־ServerGame.
from server.bus.event import Event
from server.bus.event_type import EventType


class GameSession:
    """
    Represents one running multiplayer game.

    Responsible only for:
    - storing game information
    - forwarding moves
    - exposing snapshots
    - publishing game events

    Does not know:
    - networking
    - database
    - authentication
    """

    # Create a new game session.
    def __init__(
        self,
        room,
        server_game,
        bus
    ):
        """
        Initialize one running game.
        """

        self.room = room
        self.server_game = server_game
        self.bus = bus
        self.finished = False

    # Execute one player move.
    def make_move(
        self,
        move
    ):
        """
        Forward move to ServerGame.
        """

        if self.finished:
            return None

        result = self.server_game.make_move(move)

        if result.success:

            self.bus.publish(
                Event(
                    EventType.MOVE_ACCEPTED,
                    {
                        "room_id": self.room.room_id,
                        "move": move
                    }
                )
            )

        else:

            self.bus.publish(
                Event(
                    EventType.MOVE_REJECTED,
                    {
                        "room_id": self.room.room_id,
                        "move": move
                    }
                )
            )

        return result

    # Finish the current game.
    def finish(self):
        """
        Mark game as finished.
        """

        self.finished = True

    # Return current game snapshot.
    def get_snapshot(self):
        """
        Return latest game snapshot.
        """

        return self.server_game.get_snapshot()

    # Return all players inside this game.
    def get_players(self):
        """
        Return white and black sessions.
        """

        return (
            self.room.white_player,
            self.room.black_player
        )

# from server.bus.event import Event
# from server.bus.event_type import EventType



# class GameSession:
#     """
#     Represents one active game session.

#     Responsible for:
#     - connecting players to a game
#     - forwarding moves
#     - storing game state

#     Does not know:
#     - networking
#     - database
#     - authentication
#     """



#     # Create new game session.
#     def __init__(
#         self,
#         room,
#         server_game,
#         bus
#     ):
#         """
#         Initialize game session.
#         """

#         self.room = room

#         self.server_game = server_game

#         self.bus = bus

#         self.finished = False



#     # Handle player move.
#     def make_move(
#         self,
#         move,
#         player=None
#     ):
#         """
#         Forward move to game engine.
#         """


#         if self.finished:

#             return None



#         result = (
#             self.server_game
#             .make_move(move)
#         )



#         if result.success:

#             self.bus.publish(

#                 Event(

#                     EventType.MOVE_ACCEPTED,

#                     {
#                         "room_id":
#                         self.room.room_id,


#                         "move":
#                         move

#                     }

#                 )

#             )

#         else:

#             self.bus.publish(

#                 Event(

#                     EventType.MOVE_REJECTED,

#                     {
#                         "move":
#                         move
#                     }

#                 )

#             )


#         return result

#     # Finish game.
#     def finish(
#         self
#     ):
#         """
#         Mark game as finished.
#         """

#         self.finished = True

#             # Return current game snapshot.
#     def get_snapshot(
#         self
#     ):
#         """
#         Return current state
#         of the running game.
#         """

#         return self.server_game.get_snapshot()