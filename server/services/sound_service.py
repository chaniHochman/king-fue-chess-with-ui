#מודיעה ללקוח איזה צליל לנגן
from server.bus.event import Event
from server.bus.event_type import EventType


class SoundService:
    """
    Publishes sound events.

    This service does not play sounds.

    It only informs clients which sound should be played.
    """

    # Create sound service.
    def __init__(self, bus):

        self.bus = bus

        self.register_events()

    # Subscribe to game events.
    def register_events(self):

        self.bus.subscribe(
            EventType.MOVE_ACCEPTED,
            self.play_move_sound
        )

        self.bus.subscribe(
            EventType.GAME_FINISHED,
            self.play_end_sound
        )

    # Publish move sound.
    def play_move_sound(self, event):

        self.bus.publish(

            Event(

                EventType.PLAY_SOUND,

                {
                    "sound": "move.wav"
                }

            )

        )

    # Publish end game sound.
    def play_end_sound(self, event):

        self.bus.publish(

            Event(

                EventType.PLAY_SOUND,

                {
                    "sound": "victory.wav"
                }

            )

        )