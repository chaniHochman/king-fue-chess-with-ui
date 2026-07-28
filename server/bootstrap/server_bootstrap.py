#  bus מסרים.
# מסד נתונים של יצרן.
# שירותים יוצרים.
# מחברת ביניאם.

from server.bus.message_bus import MessageBus

from server.database.database import Database

from server.authentication.auth_service import AuthService
from server.rooms.room_service import RoomService
from server.game.game_service import GameService
from server.services.score_service import ScoreService
from server.services.logger_service import LoggerService
from server.services.sound_service import SoundService
from server.services.animation_service import AnimationService
from server.services.response_service import ResponseService
from server.services.game_state_service import GameStateService

from server.game.game_manager import GameManager
from server.game.game_factory import GameFactory
from server.game.game_engine_factory import GameEngineFactory

from server.room.room_manager import RoomManager
from server.session.session_manager import SessionManager



class ServerBootstrap:
    """
    Creates and connects server components.

    Responsible for:
    - dependency creation
    - service connection

    Does not know:
    - game rules
    - UI
    - client logic
    """



    # Initialize server.
    def __init__(
        self
    ):
        """
        Build server architecture.
        """

        self.bus = MessageBus()

        self.database = Database()


        self.session_manager = SessionManager()


        self.room_manager = RoomManager(
            self.bus
        )


        self.game_factory = GameFactory(
            self.bus
        )


        self.engine_factory = GameEngineFactory()


        self.game_manager = GameManager(
            self.bus,
            self.game_factory
        )


        self.create_services()



    # Create all services.
    def create_services(
        self
    ):
        """
        Initialize server services.
        """


        self.auth_service = AuthService(
            self.bus,
            self.database
        )


        self.room_service = RoomService(
            self.bus,
            self.room_manager
        )


        self.game_service = GameService(
            self.bus,
            self.game_manager,
            self.room_manager,
            self.engine_factory
        )


        self.score_service = ScoreService(
            self.bus,
            self.database
        )


        self.logger_service = LoggerService(
            self.bus
        )


        self.sound_service = SoundService(
            self.bus
        )


        self.animation_service = AnimationService(
            self.bus
        )


        self.response_service = ResponseService(
            self.bus
        )


        self.game_state_service = GameStateService(
            self.bus,
            self.game_manager
        )