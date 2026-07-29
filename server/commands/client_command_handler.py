from server.bus.event import Event
from server.bus.event_type import EventType


class ClientCommandHandler:
    """
    Converts client messages
    into server events.

    Responsible only for:
    - parsing commands
    - publishing events
    """



    # Initialize handler.
    def __init__(
        self,
        bus,
        session_manager=None
    ):

        self._bus = bus

        self._session_manager = session_manager



    # Handle incoming client message.
    def handle(
        self,
        event
    ):
        """
        Convert network message
        into internal server event.
        """

        message = event.data["message"]

        connection = event.data["connection"]


        command = message["type"]

        data = message.get(
            "data",
            {}
        )


        mapping = {

            "login":
            EventType.LOGIN_REQUEST,


            "register":
            EventType.REGISTER_REQUEST,


            "match":
            EventType.MATCH_REQUEST,


            "create_room":
            EventType.CREATE_ROOM_REQUEST,


            "join_room":
            EventType.JOIN_ROOM_REQUEST,


            "move":
            EventType.MOVE_REQUESTED

        }



        event_type = mapping.get(
            command
        )


        if event_type is None:
            return



        new_data = data.copy()

        new_data["connection"] = connection



        self._bus.publish(

            Event(

                event_type,

                new_data

            )

        )