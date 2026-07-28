
from server.bootstrap.server_bootstrap import ServerBootstrap

from server.commands.client_command_handler import ClientCommandHandler

from server.services.client_message_service import ClientMessageService

from server.network.tcp_server import TCPServer



class ServerMain:
    """
    Starts multiplayer server.

    Responsible for:
    - starting server
    - connecting components

    Does not know:
    - game logic
    - authentication
    """



    # Initialize server.
    def __init__(
        self
    ):
        """
        Build server.
        """

        self.bootstrap = ServerBootstrap()


        self.command_handler = ClientCommandHandler(
            self.bootstrap.bus,
            self.bootstrap.session_resolver

        )


        self.client_message_service = ClientMessageService(
            self.bootstrap.bus,
            self.command_handler
        )


        self.server = TCPServer(
            self.bootstrap.bus,
            self.bootstrap.connection_manager
        )



    # Start server.
    def start(
        self
    ):
        """
        Run TCP server.
        """

        self.server.start()



if __name__ == "__main__":

    server = ServerMain()

    server.start()