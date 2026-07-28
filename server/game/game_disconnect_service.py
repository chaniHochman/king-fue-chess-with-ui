# לקבל PLAYER_TIMEOUT
# למצוא את המשחק של השחקן
# לסיים את המשחק
# לקבוע מנצח ומפסיד
# לפרסם GAME_FINISHED

from server.bus.event import Event
from server.bus.event_type import EventType


class GameDisconnectService:
    """
    Handles game ending because
    of player disconnect timeout.

    Responsible for:
    - finding opponent
    - finishing game
    - publishing game result

    Does not know:
    - database
    - networking
    - rating calculation
    """



    # Initialize disconnect game service.
    def __init__(
        self,
        bus,
        game_manager
    ):
        """
        Store dependencies
        and register listeners.
        """

        self._bus = bus

        self._game_manager = game_manager

        self.register_events()



    # Register timeout listener.
    def register_events(self):
        """
        Subscribe to player timeout events.
        """

        self._bus.subscribe(
            EventType.PLAYER_TIMEOUT,
            self.handle_timeout
        )



    # Handle disconnected player.
    def handle_timeout(
        self,
        event
    ):
        """
        Finish game after
        disconnect timeout.
        """

        session = event.data["session"]


        room = session.room


        if room is None:
            return


        game = self._game_manager.get_game(
            room.room_id
        )


        if game is None:
            return



        white = room.white_player

        black = room.black_player



        if session == white:

            winner = black

            loser = white


        elif session == black:

            winner = white

            loser = black


        else:

            return



        game.finish()



        self._bus.publish(

            Event(

                EventType.GAME_FINISHED,

                {
                    "winner":
                    winner.user.username,

                    "loser":
                    loser.user.username,

                    "reason":
                    "disconnect_timeout"
                }

            )

        )