from types import SimpleNamespace

from logic.model.move_result import MoveResult
from server.bus.message_bus import MessageBus
from server.game.game_manager import GameManager


class FakeGameEngine:
    def request_move(self, source, target):
        return MoveResult(True, "ok")

    def wait(self, ms):
        return None

    def create_snapshot(self):
        return {"state": "ready"}

    def notify_king_captured(self):
        return None


bus = MessageBus()
manager = GameManager(bus)
room = SimpleNamespace(room_id="room-1")
created = manager.create_game(room, FakeGameEngine())
result = manager.handle_move("room-1", ("a1", "a2"))
print(type(created).__name__)
print(bool(result), result.reason)
