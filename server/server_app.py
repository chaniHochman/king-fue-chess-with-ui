from server.bus.message_bus import MessageBus

from server.database.database import Database

from server.session.session_manager import SessionManager
from server.session.session_service import SessionService
from server.session.session_resolver import SessionResolver

from server.rooms.room_manager import RoomManager

from server.game.game_manager import GameManager

from server.services.logger_service import LoggerService
from server.services.score_service import ScoreService
from server.services.sound_service import SoundService
from server.services.animation_service import AnimationService

from server.authentication.auth_service import AuthService

from server.network.tcp_server import TCPServer
from server.network.connection_manager import ConnectionManager

from server.commands.client_command_handler import ClientCommandHandler

from server.bus.event_type import EventType


class ServerApp:
    """
    Main server composition root.

    Responsible only for creating
    and connecting server components.
    """



    # Initialize complete server.
    def __init__(self):
        """
        Create all server dependencies.
        """


        # Central communication system
        self.bus = MessageBus()



        # Database layer
        self.database = Database()



        # Connection management
        self.connection_manager = ConnectionManager()



        # Online users
        self.session_manager = SessionManager()



        # Authentication
        self.auth_service = AuthService(
            self.bus,
            self.database
        )



        # Sessions
        self.session_service = SessionService(
            self.bus,
            self.session_manager
        )


        self.session_resolver = SessionResolver(
            self.bus,
            self.session_manager
        )



        # Rooms
        self.room_manager = RoomManager(
            self.bus
        )



        # Games
        self.game_manager = GameManager(
            self.bus
        )



        # Server services

        self.logger = LoggerService(
            self.bus
        )


        self.score = ScoreService(
            self.bus,
            self.database
        )


        self.sound = SoundService(
            self.bus
        )


        self.animation = AnimationService(
            self.bus
        )



        # Client command translation

        self.command_handler = ClientCommandHandler(
            self.bus,
            self.session_manager
        )



        self.register_events()



        # Network server

        self.server = TCPServer(
            "localhost",
            5000,
            self.connection_manager,
            self.bus
        )

    # Register global server listeners.
    def register_events(self):
        """
        Connect external events
        into the server system.
        """

        self.bus.subscribe(
            EventType.CLIENT_MESSAGE,
            self.command_handler.handle
        )

    # Start server.
    def start(self):
        """
        Start network server.
        """

        self.server.start()