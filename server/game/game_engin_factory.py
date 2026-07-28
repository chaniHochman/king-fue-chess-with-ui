from server.game.score_data import ScoreData
from server.game.moves_log import MovesLog

from logic.input_output.BoardParser import BoardParser
from logic.rules.rule_engine import RuleEngine
from logic.realtime.real_time_arbiter import RealTimeArbiter
from logic.engine.game_engine import GameEngine


class GameEngineFactory:
    """
    Creates complete game engines.

    Responsible only for:
    - creating board
    - creating rule engine
    - creating realtime arbiter
    - creating server score data
    - creating server moves log
    - creating game engine

    Does not know:
    - networking
    - rooms
    - sessions
    - database
    """


    # Create a new isolated game engine.
    def create_engine(
        self
    ):
        """
        Build all game logic objects.
        """


        parser = BoardParser()


        board = parser.parse_to_board(
            """
            bR bN bB bQ bK bB bN bR
            bP bP bP bP bP bP bP bP
            .  .  .  .  .  .  .  .
            .  .  .  .  .  .  .  .
            .  .  .  .  .  .  .  .
            .  .  .  .  .  .  .  .
            wP wP wP wP wP wP wP wP
            wR wN wB wQ wK wB wN wR
            """
        )


        rule_engine = RuleEngine(
            board
        )


        score_data = ScoreData()


        moves_log = MovesLog()


        arbiter = RealTimeArbiter(
            board
        )


        engine = GameEngine(
            board,
            rule_engine,
            arbiter,
            score_data,
            moves_log
        )


        arbiter.set_game_engine(
            engine
        )


        return engine