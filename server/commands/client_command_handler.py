# הוא רק מתרגם הודעה → Event.
#
# הוא לא מכיל לוגיקה של:
# משתמשים
# חדרים
# משחקים
#
# הוא מקבל הודעה מהלקוח
# ומפרסם Event דרך MessageBus.


from server.bus.event import Event

from server.bus.event_type import EventType

from server.common.message_type import MessageType

class ClientCommandHandler:
    """
    Converts client messages
    into server events.

    Does not contain business logic.
    """
    # Creates command handler.
    def __init__(
        self,
        bus,
        session_manager
    ):
        """
        Initialize command handler.

        Stores MessageBus and SessionManager.
        """

        self._bus = bus

        self._session_manager = session_manager



    # Handles client message event.
    def handle(
        self,
        event
    ):
        """
        Receive client message
        and convert it into server event.
        """

        connection = event.data["connection"]

        message = event.data["message"]


        message_type = message.type

        payload = message.payload



        if message_type == MessageType.LOGIN:

            self._handle_login(
                connection,
                payload
            )



        elif message_type == MessageType.REGISTER:

            self._handle_register(
                connection,
                payload
            )



        elif message_type == MessageType.CREATE_ROOM:

            self._handle_create_room(
                connection
            )



        elif message_type == MessageType.JOIN_ROOM:

            self._handle_join_room(
                connection,
                payload
            )



        elif message_type == MessageType.PLAY:

            self._handle_play(
                connection
            )



        elif message_type == MessageType.MOVE:

            self._handle_move(
                connection,
                payload
            )



    # Find session by client connection.
    def get_session(
        self,
        connection
    ):
        """
        Return the active session
        that belongs to this connection.
        """

        sessions = (
            self._session_manager.get_all_sessions()
        )


        for session in sessions:

            if session.connection == connection:

                return session



        return None



    # Creates login request event.
    def _handle_login(
        self,
        connection,
        payload
    ):
        """
        Publish login request.
        """


        self._bus.publish(

            Event(

                EventType.LOGIN_REQUEST,

                {
                    "connection": connection,

                    "username":
                    payload["username"],

                    "password":
                    payload["password"]
                }

            )

        )



    # Creates register request event.
    def _handle_register(
        self,
        connection,
        payload
    ):
        """
        Publish register request.
        """


        self._bus.publish(

            Event(

                EventType.REGISTER_REQUEST,

                {
                    "connection": connection,

                    "username":
                    payload["username"],

                    "password":
                    payload["password"]
                }

            )

        )



    # Creates room creation request event.
    def _handle_create_room(
        self,
        connection
    ):
        """
        Publish room creation request
        with current session.
        """


        session = self.get_session(
            connection
        )


        self._bus.publish(

            Event(

                EventType.CREATE_ROOM_REQUEST,

                {
                    "connection": connection,

                    "session": session
                }

            )

        )



    # Creates join room request event.
    def _handle_join_room(
        self,
        connection,
        payload
    ):
        """
        Publish join room request
        with current session.
        """
        # session = self.get_session(
        #     connection
        # )

        self._bus.publish(

            Event(

                EventType.JOIN_ROOM_COMMAND,

                {
                    "connection": connection,

                    # "session": session,

                    "room_id":
                    payload["room_id"]
                }

            )

        )



    # Creates move request event.
    def _handle_move(
        self,
        connection,
        payload
    ):
        """
        Publish move request.
        """


        session = self.get_session(
            connection
        )



        self._bus.publish(

            Event(

                EventType.MOVE_REQUESTED,

                {
                    "connection": connection,

                    "session": session,

                    "move":
                    payload["move"]
                }

            )

        )



    # Creates matchmaking request event.
    def _handle_play(
        self,
        connection
    ):
        """
        Publish matchmaking request.
        """


        session = self.get_session(
            connection
        )



        self._bus.publish(

            Event(

                EventType.MATCH_REQUEST,

                {
                    "connection": connection,

                    "session": session
                }

            )

        )