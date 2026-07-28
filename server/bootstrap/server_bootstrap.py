from server.bus.message_bus import MessageBus

from server.database.database import Database


from server.session.session_manager import SessionManager
from server.session.session_resolver import SessionResolver


from server.rooms.room_manager import RoomManager

from server.game.game_manager import GameManager
from server.game.game_factory import GameFactory
from server.game.game_engin_factory import GameEngineFactory


from server.authentication.auth_service import AuthService

from server.rooms.room_service import RoomService

from server.game.game_service import GameService

from server.services.score_service import ScoreService
from server.services.logger_service import LoggerService
from server.services.sound_service import SoundService
from server.services.animation_service import AnimationService
from server.services.response_service import ResponseService
from server.services.game_state_service import GameStateService


from server.commands.client_command_handler import ClientCommandHandler

from server.services.client_message_service import ClientMessageService

from server.network.tcp_server import TCPServer

from server.network.connection_manager import ConnectionManager

from server.services.matchmaking_service import MatchmakingService

class ServerBootstrap:
    """
    Creates complete server architecture.

    Responsible for:
    - creating components
    - connecting dependencies

    Does not know:
    - game rules
    - UI
    """



    # Initialize server.
    def __init__(
        self
    ):
        """
        Build server objects.
        """


        self.bus = MessageBus()


        self.database = Database()

        

        # Sessions

        self.session_manager = SessionManager()


        self.session_resolver = SessionResolver(
            self.bus,
            self.session_manager
        )



        # Rooms

        self.room_manager = RoomManager()



        # Games

        self.engine_factory = GameEngineFactory()


        self.game_factory = GameFactory(
            self.bus,
            self.engine_factory
        )


        self.game_manager = GameManager(
            self.bus,
            self.game_factory
        )



        self.create_services()


        self.create_network()




    # Create server services.
    def create_services(
        self
    ):
        """
        Create all services.
        """
        


        self.auth_service = AuthService(
            self.bus,
            self.database
        )


        self.room_service = RoomService(
            self.bus,
            self.room_manager
        )
        self.matchmaking_service = MatchmakingService(
                    self.bus
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



    # Create network layer.
    def create_network(
        self
    ):
        """
        Create communication objects.
        """


        self.connection_manager = ConnectionManager()



        self.command_handler = ClientCommandHandler(
            self.bus,
            self.session_resolver
        )



        self.client_message_service = ClientMessageService(
            self.bus,
            self.command_handler
        )



        self.tcp_server = TCPServer(
            self.bus,
            self.connection_manager
        )