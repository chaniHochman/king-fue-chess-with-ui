from server.bus.message_bus import MessageBus

from server.database.database import Database

from server.authentication.auth_service import AuthService

from server.session.session_manager import SessionManager
from server.session.session_service import SessionService
from server.session.session_resolver import SessionResolver
from server.session.session_disconnect_service import SessionDisconnectService
from server.session.reconnect_service import ReconnectService

from server.rooms.room_manager import RoomManager
from server.rooms.room_service import RoomService

from server.game.game_manager import GameManager
from server.game.game_service import GameService
from server.game.game_factory import GameFactory
from server.game.game_engin_factory import GameEngineFactory

from server.services.logger_service import LoggerService
from server.services.score_service import ScoreService
from server.services.sound_service import SoundService
from server.services.animation_service import AnimationService

from server.network.connection_manager import ConnectionManager
from server.network.tcp_server import TCPServer

from server.commands.client_command_handler import ClientCommandHandler

from server.services.disconnect_monitor import DisconnectMonitor
from server.bus.event_type import EventType
from server.services.response_service import ResponseService
from server.services.matchmaking_service import MatchmakingService


class ServerApp:
    """
    Creates and connects all server components.

    Responsible only for:
    - dependency creation
    - service wiring

    Does not know:
    - game rules
    - authentication logic
    """



    # Initialize server.
    def __init__(
        self
    ):
        """
        Build complete server.
        """

        # Central communication channel.
        self.bus = MessageBus()



        # Database.
        self.database = Database()



        # Network connections.
        self.connection_manager = ConnectionManager()



        # User sessions.
        self.session_manager = SessionManager()



        # Authentication.
        self.auth_service = AuthService(
            self.bus,
            self.database
            
        )



        # Session creation after login.
        self.session_service = SessionService(
            self.bus,
            self.session_manager
        )



        # Resolve connection -> session.
        self.session_resolver = SessionResolver(
            self.bus,
            self.session_manager
        )



        # Disconnect handling.
        self.disconnect_service = SessionDisconnectService(
            self.bus,
            self.session_manager
        )



        # Reconnect handling.
        self.reconnect_service = ReconnectService(
            self.bus,
            self.session_manager
        )



        # Rooms.
        self.room_manager = RoomManager()


        self.room_service = RoomService(
            self.bus,
            self.room_manager
        )



        # Game creation.
        self.game_engine_factory = GameEngineFactory()


        self.game_factory = GameFactory(
            self.bus,
            self.game_engine_factory
        )



        self.game_manager = GameManager(
            self.bus,
            self.game_factory
        )



        self.game_service = GameService(
            self.bus,
            self.game_manager,
            self.room_manager
        )



        # Background services.
        self.logger_service = LoggerService(
            self.bus
        )


        self.score_service = ScoreService(
            self.bus,
            self.database
        )


        self.sound_service = SoundService(
            self.bus
        )


        self.animation_service = AnimationService(
            self.bus
        )



        # Disconnect timer.
        self.disconnect_monitor = DisconnectMonitor(
            self.bus,
            self.session_manager
        )



        # Client command translation.
        self.command_handler = ClientCommandHandler(
            self.bus
        )
        self.response_service = ResponseService(
            self.bus
        )
        self.matchmaking_service = MatchmakingService(
                self.bus
            )

        self.bus.subscribe(
            EventType.CLIENT_MESSAGE,
            self.command_handler.handle
        )



        # TCP communication.
        self.server = TCPServer(
            "localhost",
            5000,
            self.connection_manager,
            self.bus
        )



    # Start server.
    def start(
        self
    ):
        """
        Start background services
        and network server.
        """

        self.disconnect_monitor.start()

        self.server.start()



    # Stop server.
    def stop(
        self
    ):
        """
        Shutdown server.
        """

        self.disconnect_monitor.stop()

        self.server.stop()

        self.connection_manager.close_all()