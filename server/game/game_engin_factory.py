from logic.model.board import Board
from logic.rules.rule_engine import RuleEngine
from logic.realtime.real_time_arbiter import RealTimeArbiter
from logic.engine.game_engine import GameEngine



class GameEngineFactory:
    """
    Creates game engines.

    Responsible for:
    - building logic components
    - connecting dependencies

    Does not know:
    - rooms
    - players
    - network
    """



    # Initialize factory.
    def __init__(
        self,
        score_data=None,
        moves_log=None
    ):
        """
        Store optional game services.
        """

        self.score_data = score_data

        self.moves_log = moves_log



    # Create new game engine.
    def create_engine(
        self
    ):
        """
        Build complete GameEngine.
        """


        board = Board()



        rule_engine = RuleEngine(
            board
        )



        real_time_arbiter = RealTimeArbiter(
            board
        )



        game_engine = GameEngine(

            board,

            rule_engine,

            real_time_arbiter,

            self.score_data,

            self.moves_log

        )



        real_time_arbiter.set_game_engine(
            game_engine
        )



        return game_engine