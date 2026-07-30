from logic.model.position import Position


class Piece:
    """מייצג כלי שחמט עם מאפיינים בסיסיים של זהות, צבע, סוג, מיקום וסטטוס."""

    _used_ids = set()
    _valid_colors = {"white", "black"}
    _valid_kinds = {"king", "queen", "rook", "bishop", "knight", "pawn"}
    _valid_states = { "idle","move","jump","short_rest","long_rest"}

    def __init__(self, piece_id: int, color: str, kind: str, cell: Position, state: str = "idle"):
        """יוצר כלי חדש ומאמת שהנתונים תקינים ושהמזהה ייחודי."""
        self._validate_id(piece_id)
        self._validate_color(color)
        self._validate_kind(kind)
        self._validate_cell(cell)
        self._validate_state(state)

        self.piece_id = piece_id
        self.color = color
        self.kind = kind
        self.cell = cell
        self.state = state
        Piece._used_ids.add(piece_id)
    
    
    @property
    def id(self):
        """
        Returns the unique identifier of the piece.
        Used by external systems such as animation and rendering.
        """
        return self.piece_id
    
    def _validate_id(self, id: int):
        """מאמת שמזהה הכלי הוא מספר שלם וייחודי."""
        if not isinstance(id, int):
            raise TypeError("id must be an int")
        if id in Piece._used_ids:
            raise ValueError("piece id must be unique")

    def _validate_color(self, color: str):
        """מאמת שהצבע הוא אחד הערכים המותרים."""
        if color not in self._valid_colors:
            raise ValueError("color must be 'white' or 'black'")

    def _validate_kind(self, kind: str):
        """מאמת שהסוג הוא אחד מסוגי הכלים המותרים."""
        if kind not in self._valid_kinds:
            raise ValueError("kind must be one of: king, queen, rook, bishop, knight, pawn")

    def _validate_cell(self, cell: Position):
        """מאמת שהמיקום של הכלי הוא אובייקט Position."""
        if not isinstance(cell, Position):
            raise TypeError("cell must be a Position")

    def _validate_state(self, state: str):
        """מאמת שהמצב הוא אחד מהמצבים המותרים."""
        if state not in self._valid_states:
            raise ValueError(
                        "state must be one of: idle, move, jump, short_rest, long_rest"
                    )
    def __repr__(self):
        """מחזיר ייצוג קריא של הכלי לצורך הדפסה וניתוח."""
        return (
            f"Piece(id={self.piece_id}, color={self.color!r}, kind={self.kind!r}, "
            f"cell={self.cell!r}, state={self.state!r})"
        )
