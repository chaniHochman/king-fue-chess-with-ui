#מודיעה ללקוח איזו אנימציה להפעיל
from server.bus.event import Event
from server.bus.event_type import EventType


class AnimationService:
    """
    Handles animation events.

    Responsible for:
    - receiving animation requests
    - publishing animation events

    Does not know:
    - UI
    - rendering
    - networking
    """


    # Initialize animation service.
    def __init__(
        self,
        bus
    ):
        """
        Store bus.
        """

        self._bus = bus

        self.register_events()



    # Register animation events.
    def register_events(self):
        """
        Subscribe to game animation triggers.
        """

        self._bus.subscribe(
            EventType.MOVE_ACCEPTED,
            self.handle_move_animation
        )



    # Create move animation event.
    def handle_move_animation(
        self,
        event
    ):
        """
        Publish animation request.
        """

        self._bus.publish(
            Event(
                EventType.PLAY_ANIMATION,
                {
                    "animation":
                    "piece_move",

                    "move":
                    event.data["move"]
                }
            )
        )