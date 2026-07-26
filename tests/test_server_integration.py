from types import SimpleNamespace

from logic.model.move_result import MoveResult
from server.bus.message_bus import MessageBus
from server.game.game_manager import GameManager


class FakeGameEngine:
    def __init__(self):
        self.moves = []

    def request_move(self, source, target):
        self.moves.append((source, target))
        return MoveResult(True, "ok")

    def wait(self, ms):
        return None

    def create_snapshot(self):
        return {"state": "ready"}

    def notify_king_captured(self):
        return None


def test_game_manager_routes_moves_to_game_engine():
    bus = MessageBus()
    manager = GameManager(bus)
    room = SimpleNamespace(room_id="room-1")

    game_session = manager.create_game(room, FakeGameEngine())

    assert manager.get_game("room-1") is game_session

    result = manager.handle_move("room-1", ("a1", "a2"))

    assert result is not None
    assert bool(result) is True
    assert result.reason == "ok"
