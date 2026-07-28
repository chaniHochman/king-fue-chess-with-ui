# המחלקה אחראית על כל הפעולות הקשורות למשתמשים:

# הרשמת משתמש חדש.
# התחברות.
# בדיקה האם המשתמש כבר קיים.
# טעינת נתוני המשתמש.

# היא לא פונה ישירות ל־TCP Server, אלא עובדת מול ה־Database ומפרסמת תוצאות ל־MessageBus.

import hashlib

from server.authentication.user import User
from server.bus.event import Event
from server.bus.event_type import EventType


class AuthService:
    """
    Handles user registration and login operations.

    Responsible only for:
    - checking users
    - creating users
    - validating passwords

    Communicates with:
    - Database
    - MessageBus

    It does not handle network communication directly.
    """

    # Initialize authentication service.
    def __init__(
        self,
        bus,
        database
    ):
        """
        Initialize authentication service.

        Saves database and bus references,
        then subscribes to authentication events.
        """
        self.bus = bus
        self.database = database
        

        self.register_events()


    # Register authentication event handlers.
    def register_events(self):
        """
        Subscribe login and register requests
        to the MessageBus.
        """

        self.bus.subscribe(
            EventType.LOGIN_REQUEST,
            self.handle_login
        )

        self.bus.subscribe(
            EventType.REGISTER_REQUEST,
            self.handle_register
        )


    # Handle login request event.
    def handle_login(
        self,
        event
    ):
        """
        Receive login request from MessageBus
        and call login logic.
        """

        connection = event.data["connection"]

        username = event.data["username"]

        password = event.data["password"]


        self.login(
            connection,
            username,
            password
        )


    # Handle register request event.
    def handle_register(
        self,
        event
    ):
        """
        Receive register request from MessageBus
        and call registration logic.
        """

        connection = event.data["connection"]

        username = event.data["username"]

        password = event.data["password"]


        self.register(
            connection,
            username,
            password
        )


    # Register a new user.
    def register(
        self,
        connection,
        username,
        password
    ):
        """
        Create a new user.

        Checks if username exists,
        saves password hash,
        and publishes result event.
        """

        existing_user = self.database.get_user(username)


        if existing_user:

            self.bus.publish(
                Event(
                    EventType.LOGIN_FAILED,
                    {
                        "connection": connection,
                        "reason": "username_exists"
                    }
                )
            )

            return False


        password_hash = self.hash_password(password)


        self.database.save_user(
            username,
            password_hash
        )

        new_user = User(
            username,
            password_hash,
            1200
        )
        self.bus.publish(
            Event(
                EventType.LOGIN_SUCCESS,
                {
                    "connection": connection,
                    "user": new_user
                }
            )
        )


        return True



    # Authenticate existing user.
    def login(
        self,
        connection,
        username,
        password
    ):
        """
        Authenticate existing user.

        Checks username and password,
        then publishes success or failure event.
        """

        user = self.database.get_user(username)


        if not user:

            self.bus.publish(
                Event(
                    EventType.LOGIN_FAILED,
                    {
                        "connection": connection,
                        "reason": "user_not_found"
                    }
                )
            )

            return None



        stored_hash = user[2]


        password_hash = self.hash_password(password)


        if password_hash != stored_hash:

            self.bus.publish(
                Event(
                    EventType.LOGIN_FAILED,
                    {
                        "connection": connection,
                        "reason": "wrong_password"
                    }
                )
            )

            return None



        logged_user = User(
            user[1],
            user[2],
            user[3]
        )


        self.bus.publish(
            Event(
                EventType.LOGIN_SUCCESS,
                {
                    "connection": connection,
                    "user": logged_user
                }
            )
        )


        return logged_user



    # Create password hash.
    def hash_password(
        self,
        password
    ):
        """
        Convert plain password into secure hash.
        """

        return hashlib.sha256(
            password.encode()
        ).hexdigest()