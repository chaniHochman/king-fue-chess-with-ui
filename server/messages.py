import json


class Message:
    """
    Represents client-server message.

    Responsible for:
    - message type
    - message data
    - serialization

    Does not know:
    - network
    - game logic
    """


    SEPARATOR = "\n"



    # Initialize message.
    def __init__(
        self,
        message_type,
        data=None
    ):
        """
        Store message data.
        """

        self.type = message_type

        self.data = data or {}



    # Convert message to dictionary.
    def to_dict(
        self
    ):
        """
        Create JSON structure.
        """

        return {

            "type": self.type.value if hasattr(self.type, "value") else self.type,
            "data": self.data

        }



    # Encode message.
    def encode(
        self
    ):
        """
        Convert message into TCP format.
        """

        return (
            json.dumps(
                self.to_dict()
            )
            +
            self.SEPARATOR
        ).encode("utf-8")



    # Decode message.
    @staticmethod
    def decode(
        raw
    ):
        """
        Create message from JSON.
        """

        data = json.loads(
            raw
        )


        return Message(

            data["type"],

            data.get(
                "data",
                {}
            )

        )