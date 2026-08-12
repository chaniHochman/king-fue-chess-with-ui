# הוא לא מצייר בעצמו.

# הוא רק אומר לכל אחד מתי לעבוד.isplayManager – חיבור הכול: לולאת המשחק, עדכון (update), ציור (render), קליטת עכבר והצגת המסך.
import cv2
from UI.graphics.img import Img
from UI.graphics.config import FRAME_DELAY_MS
from logic.model.game_snapshot import GameSnapshot, PieceSnapshot
class DisplayManager:

    def __init__(
        self,
        game_engine,
        board_loader,
        board_renderer,
        piece_renderer,
        piece_animator,
        score_renderer,
        moves_renderer,
        mouse_extractor,
        command_sender,
        tcp_client=None
    ):

        self._game_engine = game_engine

        self._board_loader = board_loader

        self._piece_animator = piece_animator

        self._mouse_extractor = mouse_extractor

        self._command_sender = command_sender

        self._tcp_client = tcp_client

        self._server_snapshot = None
        
        self._window_name = "KungFu Chess"
        
        self._renderers = [
            board_renderer,
            piece_renderer,
            score_renderer,
            moves_renderer
            ]

    def set_snapshot(self, snapshot):
        pieces = [
            PieceSnapshot(
                p["piece_id"],
                p["kind"],
                p["color"],
                p["pixel_x"],
                p["pixel_y"],
                p["state"],
                None
            )
            for p in snapshot["pieces"]
        ]
        self._server_snapshot = GameSnapshot(
            snapshot["board_width"],
            snapshot["board_height"],
            pieces,
            None,
            snapshot["game_over"]
        )

    #update the game
    def update(self):

        self._game_engine.wait(FRAME_DELAY_MS)

        self._piece_animator.update(FRAME_DELAY_MS)

    #build one frame
    def render(self):

        board = self._board_loader.get_image()

        hud_width = 350

        canvas = Img.create_blank(
            width=board.width() + hud_width,
            height=board.height()
        )

        board.draw_on(
            canvas,
            0,
            0
        )

        snapshot = self._server_snapshot if self._server_snapshot is not None else self._game_engine.create_snapshot()
   
        for renderer in self._renderers:
            if renderer is not None:
                renderer.render(canvas, snapshot)
        
        return canvas
  
    
    def _mouse_callback(
        self,
        event,
        x,
        y,
        flags,
        param
        ):
        command=None
        if event == cv2.EVENT_LBUTTONDOWN:

            command = self._mouse_extractor.extract_left_click(
                x,
                y
            )


        elif event == cv2.EVENT_RBUTTONDOWN:

            command = self._mouse_extractor.extract_right_click(
                x,
                y
            )

        if command is not None:

            self._command_sender.send(command)
    
    def show_frame(self,canvas):
        cv2.imshow("KungFu Chess", canvas.img)
    
    def run(self):
        cv2.namedWindow(self._window_name)
        cv2.setMouseCallback(self._window_name, self._mouse_callback)
        while not self._game_engine.is_game_over() and not (
            self._server_snapshot is not None
            and self._server_snapshot.game_over
        ):
            if self._tcp_client is not None:
                msg = self._tcp_client.get_last_message()
                if msg and msg.get("type") == "game_state":
                    self.set_snapshot(msg["data"]["snapshot"])
                    self._tcp_client.last_message = None
            self.update()
            canvas = self.render()
            self.show_frame(canvas)
            key = cv2.waitKey(1)
            if key == 27:
                break
        cv2.destroyAllWindows()