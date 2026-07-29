from server.bus.event import Event
from server.bus.event_type import EventType



class GameManager:
    """
    Manages active games.

    Responsible for:
    - storing games
    - finding games
    - forwarding commands

    Does not know:
    - game rules
    - authentication
    - networking
    """



    # Initialize game manager.
    def __init__(
        self,
        bus,
        game_factory
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._game_factory = game_factory


        self._games = {}



    # Create game.
    def create_game(
        self,
        game_id
    ):
        """
        Create and store new game.
        """


        game = self._game_factory.create_game(
            game_id
        )


        self._games[game_id] = game



        self._bus.publish(

            Event(

                EventType.GAME_CREATED,

                {
                    "game_id": game_id
                }

            )

        )


        return game



    # Get game.
    def get_game(
        self,
        game_id
    ):
        """
        Return active game.
        """

        return self._games.get(
            game_id
        )



    # Remove game.
    def remove_game(
        self,
        game_id
    ):
        """
        Delete finished game.
        """

        return self._games.pop(
            game_id,
            None
        )



    # Handle move request.
    def handle_move(
        self,
        game_id,
        source,
        target
    ):
        """
        Forward move to ServerGame.
        """


        game = self.get_game(
            game_id
        )


        if game is None:


            return False



        return game.make_move(
            source,
            target
        )



    # Return all games.
    def get_all_games(
        self
    ):
        """
        Return active games.
        """

        return list(
            self._games.values()
        )