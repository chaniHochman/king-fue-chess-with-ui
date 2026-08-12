from server.bus.event import Event
from server.bus.event_type import EventType



class GameDisconnectService:
    """
    Handles game disconnection.

    Responsible for:
    - resigning disconnected players

    Does not know:
    - authentication
    - networking
    - rating calculation
    """



    # Initialize service.
    def __init__(
        self,
        bus,
        game_manager,
        room_manager
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._game_manager = game_manager

        self._room_manager = room_manager


        self.register_events()



    # Register listeners.
    def register_events(
        self
    ):
        """
        Subscribe to disconnect timeout.
        """

        self._bus.subscribe(

            EventType.DISCONNECT_TIMEOUT,

            self.handle_disconnect

        )



    # Handle player timeout.
    def handle_disconnect(
        self,
        event
    ):
        """
        End game after timeout.
        """

        session = event.data["session"]



        game_id = getattr(

            session,

            "game_id",

            None

        )


        if game_id is None:

            return



        game = self._game_manager.get_game(
            game_id
        )


        if game is None:

            return



        game.finish()

        room = self._room_manager.get_room_by_game_id(game_id)

        if room is not None:

            snapshot = game.get_snapshot()

            self._bus.publish(

                Event(

                    EventType.GAME_STATE_CHANGED,

                    {
                        "game_id": game_id,

                        "players": room.players,

                        "snapshot": snapshot

                    }

                )

            )

        self._game_manager.remove_game(game_id)