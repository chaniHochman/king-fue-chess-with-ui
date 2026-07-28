from server.bus.event import Event
from server.bus.event_type import EventType

from server.messages import Message


class ClientCommandHandler:
    """
    Converts client messages
    into internal server events.

    Responsible for:
    - parsing client commands
    - finding session
    - publishing server events

    Does not know:
    - authentication logic
    - game rules
    - database
    """


    # Initialize command handler.
    def __init__(
        self,
        bus,
        session_resolver
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._session_resolver = session_resolver

        self.register_events()


    # Register client messages.
    def register_events(
        self
    ):
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
        Convert client command
        into internal events.
        """

        connection = event.data.get(
            "connection"
        )

        raw_message = event.data.get(
            "message"
        )

        if raw_message is None:

            return


        message = Message.from_dict(
            raw_message
        )


        # Login does not have session yet.
        if message.type.value == "login":

            self._bus.publish(

                Event(

                    EventType.LOGIN_REQUEST,

                    {
                        "connection": connection,

                        "username":
                        message.data["username"],

                        "password":
                        message.data["password"]
                    }

                )

            )

            return


        # Register does not have session yet.
        if message.type.value == "register":

            self._bus.publish(

                Event(

                    EventType.REGISTER_REQUEST,

                    {
                        "connection": connection,

                        "username":
                        message.data["username"],

                        "password":
                        message.data["password"]
                    }

                )

            )

            return


        session = self._session_resolver.get_session(
            connection
        )

        if session is None:

            return


        if message.type.value == "create_room":

            self._bus.publish(

                Event(

                    # EventType.CREATE_ROOM_REQUEST,

                    {
                        "session":session,
                        "connection": connection

                    }

                )

            )


        elif message.type.value == "join_room":

            self._bus.publish(

                Event(

                    EventType.JOIN_ROOM_REQUEST,

                    {
                        "session":
                        session,

                        "room_id":
                        message.data["room_id"]
                    }

                )

            )


        elif message.type.value == "leave_room":

            self._bus.publish(

                Event(

                    EventType.LEAVE_ROOM_REQUEST,

                    {
                        "session":
                        session
                    }

                )

            )


        elif message.type.value == "move":

            self._bus.publish(

                Event(

                    EventType.MOVE_REQUESTED,

                    {
                        "session":
                        session,

                        "move":
                        message.data["move"]
                    }

                )

            )


        elif message.type.value == "play":

            self._bus.publish(

                Event(

                    EventType.MATCH_REQUEST,

                    {
                        "session": session,

                        "rating": session.user.rating
                    }

                )

            )


        elif message.type.value == "game_state":

            self._bus.publish(

                Event(

                    EventType.GAME_STATE_CHANGED,

                    {
                        "session":
                        session
                    }

                )

            )
                # Handle message directly.
    def handle(
        self,
        event
    ):
        """
        Compatibility method.

        Called by ClientMessageService.
        Redirects handling to handle_message.
        """

        self.handle_message(
            event
        )