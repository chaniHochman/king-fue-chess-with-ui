from collections import defaultdict



class MessageBus:
    """
    Central communication system.

    Components communicate only
    through events.

    Responsible for:
    - subscribing listeners
    - publishing events

    Does not know:
    - users
    - games
    - rooms
    """



    # Initialize message bus.
    def __init__(
        self
    ):
        """
        Create empty subscribers storage.
        """

        self._subscribers = defaultdict(list)



    # Register event listener.
    def subscribe(
        self,
        event_type,
        handler
    ):
        """
        Add handler for event type.
        """

        if handler not in self._subscribers[event_type]:

            self._subscribers[event_type].append(
                handler
            )



    # Remove event listener.
    def unsubscribe(
        self,
        event_type,
        handler
    ):
        """
        Remove existing handler.
        """

        if handler in self._subscribers[event_type]:

            self._subscribers[event_type].remove(
                handler
            )



    # Publish event.
    def publish(
        self,
        event
    ):
        """
        Send event to all listeners.
        """
        print(
            "BUS PUBLISH:",
            event.type
        )
        handlers = self._subscribers.get(
            event.type,
            []
        )


        for handler in handlers:

            try:

                handler(
                    event
                )


            except Exception as error:

                print(
                    "Event handler error:",
                    error
                )



    # Return number of listeners.
    def listener_count(
        self,
        event_type
    ):
        """
        Return amount of listeners.
        """

        return len(
            self._subscribers[event_type]
        )