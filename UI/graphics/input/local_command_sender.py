#מתרגמת פקודה לקריאה למנוע
#כדי שהעכבר לא יכיר את GameEngine.
from UI.graphics.input.commands import ClickCommand, JumpCommand

class LocalCommandSender:

    def __init__(self, controller, tcp_client=None, game_id=None):
        self._controller = controller
        self._tcp_client = tcp_client
        self._game_id = game_id
        self._pending_source = None


    def send(self, command):

        if isinstance(command, ClickCommand):

            if self._tcp_client is not None:

                if self._pending_source is None:

                    piece = self._controller._game_engine.get_piece(
                        command.position
                    )

                    if piece is not None:
                        self._pending_source = command.position

                else:

                    self._tcp_client.send_move(
                        self._game_id,
                        self._pending_source,
                        command.position
                    )

                    self._pending_source = None

            else:

                self._controller.on_click(
                    command.position
                )

        elif isinstance(command, JumpCommand):

            if self._tcp_client is None:

                self._controller.on_jump(
                    command.position
                )