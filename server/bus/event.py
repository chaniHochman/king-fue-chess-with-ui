import time
import uuid


class Event:
    """
    Represents internal server event.

    Events are used only inside the server.

    Responsible for:
    - storing event type
    - storing event data
    - identifying event creation time

    Does not know:
    - network
    - database
    - game logic
    """



    # Initialize event.
    def __init__(
        self,
        event_type,
        data=None
    ):
        """
        Create new internal event.
        """

        self.id = str(uuid.uuid4())

        self.type = event_type

        self.data = data or {}

        self.timestamp = time.time()



    # Return event information.
    def to_dict(
        self
    ):
        """
        Convert event into dictionary.
        """

        return {

            "id": self.id,

            "type": self.type.value,

            "data": self.data,

            "timestamp": self.timestamp

        }