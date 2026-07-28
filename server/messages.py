#מחזיקה את מבנה ההודעות שעוברות בין:

# Client
# Server
# מייצגת הודעה אחידה בין הלקוח לשרת (סוג הודעה + נתונים).
from server.common.message_type import MessageType
import json

class Message:
    """
    Represents communication message.

    Responsible for:
    - storing message type
    - storing message data

    Does not know:
    - network
    - users
    - games
    """



    # Initialize message.
    def __init__(
        self,
        message_type,
        data
    ):
        """
        Store message information.
        """

        self.type = message_type

        self.data = data or {}



    # Convert message to dictionary.
    def to_dict(
        self
    ):
        """
        Return message representation.
        """

        return {

            "type":
            self.type.value,

            "data":
            self.data

        }



    # Create message from dictionary.
    @staticmethod
    def from_dict(
        data
    ):
        """
        Build Message object.
        """

        message_type = MessageType(
            data["type"]
        )


        return Message(

            message_type,

            data.get(
                "data",
                {}
            )

        )
    # Convert message into JSON string.
    def encode(self):
        """
        Convert message object
        into network format.
        """

        return json.dumps(
            self.to_dict()
        )