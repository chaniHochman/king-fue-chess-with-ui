from server.bus.event import Event
from server.bus.event_type import EventType



class ClientCommandHandler:
    """
    Converts client messages
    into server events.

    Responsible only for:
    - parsing client commands
    - creating server events

    Does not know:
    - authentication
    - rooms
    - games
    """



    # Initialize command handler.
    def __init__(
        self,
        bus
    ):
        """
        Store message bus reference.
        """

        self._bus = bus



    # Handle incoming client message.
    def handle(
        self,
        event
    ):
        """
        Convert client message
        into internal event.
        """

        message = event.data.get(
            "message"
        )


        connection = event.data.get(
            "connection"
        )


        if message is None:

            return



        command = message.get(
            "type"
        )


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


            "leave_room":
            EventType.LEAVE_ROOM_REQUEST,


            "move":
            EventType.MOVE_REQUESTED

        }



        event_type = mapping.get(
            command
        )



        if event_type is None:

            return



        event_data = data.copy()



        event_data["connection"] = connection



        self._bus.publish(

            Event(

                event_type,

                event_data

            )

        )