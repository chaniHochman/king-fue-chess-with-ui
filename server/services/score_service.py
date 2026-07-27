#מעדכנת דירוג ELO
#לעבור על קובץ זה ולחשב בצורה נכונה
from server.bus.event_type import EventType


class ScoreService:
    """
    Calculates and updates ELO ratings.
    """


    # Initialize score service.
    def __init__(
        self,
        bus,
        database
    ):

        self.bus = bus

        self.database = database

        self.register_events()



    # Register game events.
    def register_events(self):
        """
        Subscribe to finished games.
        """

        self.bus.subscribe(
            EventType.GAME_FINISHED,
            self.update_rating
        )



    # Update ratings after game.
    def update_rating(
        self,
        event
    ):
        """
        Calculate and save new ratings.
        """


        winner = event.data["winner"]

        loser = event.data["loser"]


        winner_rating = (
            self.database.get_rating(
                winner
            )
        )


        loser_rating = (
            self.database.get_rating(
                loser
            )
        )


        new_winner = self.calculate_elo(
            winner_rating,
            loser_rating,
            True
        )


        new_loser = self.calculate_elo(
            loser_rating,
            winner_rating,
            False
        )


        self.database.update_rating(
            winner,
            new_winner
        )


        self.database.update_rating(
            loser,
            new_loser
        )