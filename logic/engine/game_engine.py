from logic.model.move_result import MoveResult
from logic.rules.rule_engine import RuleEngine
from logic.model.position import Position
from logic.model.game_snapshot import GameSnapshot, PieceSnapshot
from logic.input.board_mapper import CELL_SIZE
# מנהל לוגיקה של משחק: מקבל מצב לוח, בודק מהלכים ומפעיל תנועות
class GameEngine:
    # יוזם את המנוע עם אובייקט לוח, מנוע חוק וארביטר לזמן
    def __init__(self, board, rule_engine: RuleEngine, real_time_arbiter,score_data,moves_log):
        self._board = board
        self._rule_engine = rule_engine
        self._real_time_arbiter = real_time_arbiter
        self._game_over = False
        self._score_data = score_data
        self._moves_log = moves_log
      

    # מחזיר האם המשחק נגמר
    def is_game_over(self):
        return self._game_over
    
    def get_piece(self, position):
        return self._board.get_piece(position)
    
    # בקשת מהלך מהמיקום source ליעד target (Positions)
    def request_move(self, source, target):
        # אם המשחק כבר הסתיים — אין לבצע מהלכים
        if self._game_over:
            return MoveResult(False, "game_over")

        # כלי יכול לקפוץ אפילו כאשר קיימות תנועות אחרות;
        # כל כלי חייב להיות במצב idle לפני שיזוז או יקפוץ
        piece = self._board.get_piece(source)
        if piece is not None and piece.state != "idle":
            return MoveResult(False, "piece_busy")

        validation = self._rule_engine.validate_move(source, target)
        # validation הוא MoveValidation
        if not validation.is_valid:
            return MoveResult(False, validation.reason)

        # אם חוקי — בקש מהארביטר להתחיל תנועה
        
        if piece is None:
            return MoveResult(False, "empty_source")

        # הארביטר עובד עם תיאורים לוגיים (row,col)
        self._real_time_arbiter.start_motion(piece, (source.row, source.col), (target.row, target.col))
        return MoveResult(True, "ok")

    # מקדם זמן מדומה
    def wait(self, ms):
        self._real_time_arbiter.advance_time(ms)
    def request_jump(self, position):
        piece = self._board.get_piece(position)
        if piece is None or piece.state != "idle":
            return MoveResult(False, "piece_busy")
        self._real_time_arbiter.start_motion(piece, (position.row, position.col), (position.row, position.col))
        return MoveResult(True, "ok")
    # נקרא כאשר המלך נאסר
    def notify_king_captured(self):
        self._game_over = True

    def set_game_over(self):
        self._game_over = True
    def create_snapshot(self):
        pieces = []
        
        #on all the board
        for row in range(self._board.rows):

            for col in range(self._board.cols):
                
                position=Position(row, col)
                
                piece = self._board.get_piece(position)

                if piece is None:
                    continue
                
                pixel_x = col * CELL_SIZE

                pixel_y = row * CELL_SIZE

                snapshot_piece = PieceSnapshot(piece.piece_id,piece.kind,piece.color,pixel_x,pixel_y,piece.state,None)

                pieces.append(snapshot_piece)

        return GameSnapshot(
            board_width=self._board.cols,
            board_height=self._board.rows,
            pieces=pieces,
            selected_cell=None,
            game_over=self._game_over
            )
    
    def add_move(
        self,
        piece,
        source,
        destination
    ):
        if self._moves_log is not None:
            self._moves_log.add_move(
                piece,
                source,
                destination
            )

    def add_capture(self, piece):
        if self._score_data is not None:
            self._score_data.add_capture(piece)