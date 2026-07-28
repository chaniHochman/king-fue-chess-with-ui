from server.bus.message_bus import MessageBus

from server.database.database import Database

from server.authentication.auth_service import AuthService

from server.session.session_manager import SessionManager
from server.session.session_service import SessionService
from server.session.session_resolver import SessionResolver

from server.rooms.room_manager import RoomManager
from server.rooms.room_service import RoomService

from server.game.game_manager import GameManager

from server.services.logger_service import LoggerService
from server.services.score_service import ScoreService
from server.services.sound_service import SoundService
from server.services.animation_service import AnimationService

from server.network.connection_manager import ConnectionManager
from server.network.tcp_server import TCPServer
from server.game.game_service import GameService
from server.commands.client_command_handler import ClientCommandHandler
from server.session.session_disconnect_service import SessionDisconnectService
from server.bus.event_type import EventType
from server.session.reconnect_service import ReconnectService
from server.session.session_disconnect_service import SessionDisconnectService

from server.game.game_disconnect_service import GameDisconnectService
from server.session.disconnect_monitor import DisconnectMonitor
from server.game.game_factory import GameFactory
from server.game.game_engin_factory import GameEngineFactory

class ServerApp:
    """
    Main server composition root.

    Creates all server components
    and connects dependencies.

    Knows:
    - what exists in the server

    Does not know:
    - game rules
    - authentication logic
    - room logic
    """


    # Initialize complete server.
    def __init__(self):
        """
        Create all components
        and connect dependencies.
        """


        # Central event communication system.
        self.bus = MessageBus()


        # Database storage layer.
        self.database = Database()

        self.game_engine_factory = GameEngineFactory(
            score_data,
            moves_log
        )


        # Network connection storage.
        self.connection_manager = ConnectionManager()


        # Active user sessions.
        self.session_manager = SessionManager()


        self.disconnect_service = SessionDisconnectService(
            self.bus,
            self.session_manager
        )
        # Authentication service.
        self.auth_service = AuthService(
            self.database,
            self.bus
        )



        # Creates sessions after login.
        self.session_service = SessionService(
            self.bus,
            self.session_manager
        )



        # Resolves connection into session.
        self.session_resolver = SessionResolver(
            self.bus,
            self.session_manager
        )

        self.session_disconnect_service = SessionDisconnectService(
            self.bus,
            self.session_manager
        )

        self.reconnect_service = ReconnectService(
            self.bus,
            self.session_manager
        )

        # Room storage manager.
        self.room_manager = RoomManager()



        # Handles room events.
        self.room_service = RoomService(
            self.bus,
            self.room_manager
        )



        # Active games manager.
        self.game_factory = GameFactory(
            self.bus
        )


        self.game_manager = GameManager(
            self.bus,
            self.game_factory
        )

        #disconnect service for games.
        self.game_disconnect_service = GameDisconnectService(
            self.bus,
            self.game_manager
        )


        self.disconnect_monitor = DisconnectMonitor(
            self.bus,
            self.session_manager
        )


        self.game_service = GameService(
            self.bus,
            self.game_manager,
            self.room_manager,
            self.game_engine_factory
        )

        # Server services.
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



        # Converts client messages into events.
        self.command_handler = ClientCommandHandler(
            self.bus,
            self.session_manager
        )



        # Receive messages from clients.
        self.bus.subscribe(
            EventType.CLIENT_MESSAGE,
            self.command_handler.handle
        )



        # TCP communication server.
        self.server = TCPServer(
            "localhost",
            5000,
            self.connection_manager,
            self.bus
        )



    # Start server.
    def start(self):
        """
        Start server.
        """

        self.disconnect_monitor.start()

        self.server.start()



    # Stop server.
    def stop(self):
        """
        Shutdown server safely.
        """
        self.disconnect_monitor.stop()

        self.server.stop()

        self.connection_manager.close_all()