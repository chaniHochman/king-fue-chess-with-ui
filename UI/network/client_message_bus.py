# from collections import defaultdict



# class ClientMessageBus:
#     """
#     Client side pub/sub system.

#     UI components subscribe.
#     Network publishes.

#     Does not know:
#     - graphics
#     - game logic
#     """



#     # Initialize bus.
#     def __init__(
#         self
#     ):
#         """
#         Create empty subscribers.
#         """

#         self._subscribers = defaultdict(list)



#     # Subscribe handler.
#     def subscribe(
#         self,
#         event_type,
#         handler
#     ):
#         """
#         Register listener.
#         """

#         self._subscribers[event_type].append(
#             handler
#         )



#     # Publish event.
#     def publish(
#         self,
#         event
#     ):
#         """
#         Notify listeners.
#         """

#         handlers = self._subscribers.get(
#             event.type,
#             []
#         )


#         for handler in handlers:

#             handler(event)