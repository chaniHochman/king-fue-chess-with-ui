from server.bus.event import Event
from server.bus.event_type import EventType


class ScoreService:
    """
    Calculates and updates ELO ratings.

    Responsible for:
    - calculating ELO changes
    - updating database ratings
    - publishing score events

    Does not know:
    - game rules
    - networking
    - authentication
    """



    # Initialize score service.
    def __init__(
        self,
        bus,
        database
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._database = database

        self._k_factor = 32

        self.register_events()



    # Register score events.
    def register_events(
        self
    ):
        """
        Subscribe to game finish event.
        """

        self._bus.subscribe(
            EventType.GAME_FINISHED,
            self.update_rating
        )



    # Update player ratings.
    def update_rating(
        self,
        event
    ):
        """
        Calculate and save new ratings.
        """

        winner = event.data.get(
            "winner"
        )

        loser = event.data.get(
            "loser"
        )


        if winner is None or loser is None:
            return



        winner_rating = (
            self._database
            .get_rating(winner)
        )


        loser_rating = (
            self._database
            .get_rating(loser)
        )


        if winner_rating is None:
            return


        if loser_rating is None:
            return



        new_winner_rating = self.calculate_elo(
            winner_rating,
            loser_rating,
            True
        )


        new_loser_rating = self.calculate_elo(
            loser_rating,
            winner_rating,
            False
        )



        self._database.update_rating(
            winner,
            new_winner_rating
        )


        self._database.update_rating(
            loser,
            new_loser_rating
        )



        self._bus.publish(

            Event(

                EventType.SCORE_UPDATED,

                {
                    "winner":
                    winner,

                    "winner_rating":
                    new_winner_rating,

                    "loser":
                    loser,

                    "loser_rating":
                    new_loser_rating
                }

            )

        )



    # Calculate new ELO rating.
    def calculate_elo(
        self,
        player_rating,
        opponent_rating,
        won
    ):
        """
        Calculate new ELO rating.
        """


        expected_score = (

            1 /

            (
                1 +

                10 **
                (
                    (
                        opponent_rating
                        -
                        player_rating
                    )
                    /
                    400
                )

            )

        )


        if won:

            actual_score = 1

        else:

            actual_score = 0



        new_rating = (

            player_rating

            +

            self._k_factor

            *

            (
                actual_score
                -
                expected_score
            )

        )


        return round(
            new_rating
        )