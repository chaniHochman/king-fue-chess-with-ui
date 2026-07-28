# לקבל הודעה שקיבלה מהלקוח.
# להעביר אותה ל-CommandHandler.

from server.bus.event import Event
from server.bus.event_type import EventType


class ClientMessageService:
    """
    Connects network messages
    with command handler.

    Responsible for:
    - receiving client messages
    - forwarding commands

    Does not know:
    - authentication
    - rooms
    - games
    """


    # Initialize service.
    def __init__(
        self,
        bus,
        command_handler
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._command_handler = command_handler

        self.register_events()



    # Register client events.
    def register_events(self):
        """
        Listen to network messages.
        """

        self._bus.subscribe(
            EventType.CLIENT_MESSAGE,
            self.handle_message
        )



    # Handle incoming message.
    def handle_message(
        self,
        event
    ):
        """
        Send message to command handler.
        """

        self._command_handler.handle(
            event
        )