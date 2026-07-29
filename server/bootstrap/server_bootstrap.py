from server.server_app import ServerApp



class ServerBootstrap:
    """
    Compatibility wrapper.

    Keeps old imports working.

    Future:
    can become dependency container.
    """



    # Initialize bootstrap.
    def __init__(
        self
    ):

        self.app = ServerApp()



    # Return message bus.
    @property
    def bus(
        self
    ):

        return self.app.bus



    @property
    def session_resolver(
        self
    ):

        return self.app.session_resolver