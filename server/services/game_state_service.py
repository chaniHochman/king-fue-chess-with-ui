from server.bus.event import Event
from server.bus.event_type import EventType


class GameStateService:
    """
    Sends game state updates.

    Responsible for:
    - creating state update events
    - requesting snapshots

    Does not know:
    - game rules
    - rendering
    - networking
    """


    # Initialize game state service.
    def __init__(
        self,
        bus,
        game_manager
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._game_manager = game_manager

        self.register_events()



    # Register game state events.
    def register_events(self):
        """
        Subscribe to move events.
        """

        self._bus.subscribe(
            EventType.MOVE_ACCEPTED,
            self.send_game_state
        )



    # Send current game state.
    def send_game_state(
        self,
        event
    ):
        """
        Create state update event.
        """

        room_id = event.data["room_id"]


        game = self._game_manager.get_game(
            room_id
        )


        if game is None:

            return


        snapshot = game.get_snapshot()


        self._bus.publish(
            Event(
                EventType.GAME_STATE_CHANGED,
                {
                    "room_id":
                    room_id,

                    "snapshot":
                    snapshot
                }
            )
        )