from datetime import datetime
import uuid


class Event:
    """
    Represents an internal server event.

    Events are passed through MessageBus.
    """


    # Create new event.
    def __init__(
        self,
        event_type,
        data=None
    ):
        """
        Store event information.
        """

        self.id = str(
            uuid.uuid4()
        )

        self.type = event_type

        self.data = data or {}

        self.time = datetime.now()

        self.resolved = False


    # Return readable event text.
    def __repr__(self):
        """
        Return debug representation.
        """

        return (
            f"Event("
            f"id={self.id}, "
            f"type={self.type}, "
            f"data={self.data}"
            f")"
        )