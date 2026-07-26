#אחראי על ניהול משחקים פעילים
# יצירת משחק חדש.
# מציאת משחק קיים.
# הוספת שחקנים.
# ניהול כמה משחקים במקביל.

from server.game.server_game import ServerGame

from server.bus.event import Event

from server.bus.event_type import EventType

from server.game.game_session import GameSession

class GameManager:
    """
    Manages all active games.
    """
    
    # Initialize game manager.
    def __init__(
        self,
        bus
    ):

        self.bus = bus

        self.games = {}

        self.register_events()

    def register_events(self):
        """
        Subscribe to move requests from the message bus.
        """

        self.bus.subscribe(
            EventType.MOVE_REQUESTED,
            self.handle_move_event
        )

    # Create game from ready room.
    def create_game(
        self,
        room,
        game_engine
    ):

        server_game = ServerGame(
            room,
            game_engine
        )


        game_session = GameSession(
            room,
            server_game,
            self.bus
        )

        self.games[
            room.room_id
        ] = game_session

        self.bus.publish(

            Event(

                EventType.GAME_STARTED,

                {
                    "room_id":
                    room.room_id,
                    "white": room.white_player,
                    "black": room.black_player,
                }

            )

        )
        return game_session

    # Find game by room id.
    def get_game(
        self,
        room_id
    ):

        return self.games.get(
            room_id
        )

    def handle_move_event(self, event):
        """
        Route a move request from the message bus to the correct game session.
        """

        session = event.data.get("session")
        move = event.data.get("move")

        if session is None or move is None:
            return None

        room_id = None
        if getattr(session, "room", None) is not None:
            room_id = session.room.room_id

        return self.handle_move(room_id, move)

    # Handle player move.
    def handle_move(
        self,
        room_id,
        move
    ):

        game = self.get_game(
            room_id
        )

        if game is None:

            return None

        result = game.make_move(
            move
        )

        if result.success:

            self.bus.publish(

                Event(

                    EventType.MOVE_ACCEPTED,

                    {
                        "room_id": room_id,
                        "move": move
                    }

                )

            )

        else:

            self.bus.publish(

                Event(

                    EventType.MOVE_REJECTED,

                    {
                        "room_id": room_id,
                        "move": move
                    }
                )
            )

        return result