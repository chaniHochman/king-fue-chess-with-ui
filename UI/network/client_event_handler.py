# from UI.network.client_event_type import ClientEventType



# class ClientEventHandler:
#     """
#     Handles events from server.

#     Responsible for:
#     - forwarding server events to UI

#     Does not know:
#     - networking
#     - game rules
#     """



#     # Initialize handler.
#     def __init__(
#         self,
#         bus,
#         display_manager
#     ):
#         """
#         Store dependencies.
#         """

#         self._display = display_manager


#         bus.subscribe(

#             ClientEventType.GAME_STATE,

#             self.update_game

#         )


#         bus.subscribe(

#             ClientEventType.ROOM_CREATED,

#             self.room_created

#         )



#     # Update board.
#     def update_game(
#         self,
#         event
#     ):
#         """
#         Send snapshot to display.
#         """

#         snapshot = event.data["snapshot"]


#         self._display.update_snapshot(
#             snapshot
#         )



#     # Room created.
#     def room_created(
#         self,
#         event
#     ):
#         """
#         Show room id.
#         """

#         room_id = event.data["room_id"]

#         self._display.show_message(

#             "Room: " + room_id

#         )