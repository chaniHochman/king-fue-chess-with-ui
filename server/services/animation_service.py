#מודיעה ללקוח איזו אנימציה להפעיל
from server.bus.event import Event
from server.bus.event_type import EventType


class AnimationService:
    """
    Publishes animation events.

    The service does not know the UI.

    It only tells the client which animation should be played.
    """

    # Create animation service.
    def __init__(self, bus):

        self.bus = bus

        self.register_events()

    # Subscribe to game events.
    def register_events(self):

        self.bus.subscribe(
            EventType.GAME_STARTED,
            self.start_animation
        )

        self.bus.subscribe(
            EventType.GAME_FINISHED,
            self.end_animation
        )

    # Publish start animation.
    def start_animation(self, event):

        self.bus.publish(

            Event(

                EventType.PLAY_ANIMATION,

                {
                    "animation": "game_start"
                }

            )

        )

    # Publish end animation.
    def end_animation(self, event):

        self.bus.publish(

            Event(

                EventType.PLAY_ANIMATION,

                {
                    "animation": "victory"
                }

            )

        )