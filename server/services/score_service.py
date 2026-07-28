from server.bus.event_type import EventType


class ScoreService:
    """
    Calculates and updates ELO ratings.

    Responsible only for:
    - calculating rating changes
    - saving new ratings

    Does not know:
    - games
    - rooms
    - networking
    """


    # Initialize score service.
    def __init__(
        self,
        bus,
        database
    ):
        """
        Store dependencies
        and register events.
        """

        self.bus = bus
        self.database = database

        self.register_events()



    # Register game finish events.
    def register_events(self):
        """
        Subscribe to finished games.
        """

        self.bus.subscribe(
            EventType.GAME_FINISHED,
            self.update_rating
        )



    # Update player ratings.
    def update_rating(
        self,
        event
    ):
        """
        Calculate and save
        new ELO ratings.
        """

        winner = event.data["winner"]

        loser = event.data["loser"]


        winner_rating = (
            self.database
            .get_rating(winner)
        )

        loser_rating = (
            self.database
            .get_rating(loser)
        )


        new_winner_rating = (
            self.calculate_elo(
                winner_rating,
                loser_rating,
                True
            )
        )


        new_loser_rating = (
            self.calculate_elo(
                loser_rating,
                winner_rating,
                False
            )
        )


        self.database.update_rating(
            winner,
            new_winner_rating
        )

        self.database.update_rating(
            loser,
            new_loser_rating
        )



    # Calculate new ELO rating.
    def calculate_elo(
        self,
        player_rating,
        opponent_rating,
        won
    ):
        """
        Calculate ELO change.

        Uses standard ELO formula.
        """

        expected = (
            1 /
            (
                1 +
                10 **
                (
                    (opponent_rating - player_rating)
                    /
                    400
                )
            )
        )


        actual = 1 if won else 0


        k_factor = 32


        return round(
            player_rating +
            k_factor *
            (
                actual - expected
            )
        )