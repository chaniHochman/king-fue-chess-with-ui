from server.bus.event import Event
from server.bus.event_type import EventType
import uuid



class GameService:
    """
    Handles game related events.

    Responsible for:
    - creating games
    - receiving move requests
    - connecting rooms and games

    Does not know:
    - game rules
    - authentication
    - network
    """



    # Initialize game service.
    def __init__(
        self,
        bus,
        game_manager,
        room_manager,
        game_engine_factory=None
    ):
        """
        Store dependencies.
        """

        self._bus = bus

        self._game_manager = game_manager

        self._room_manager = room_manager

        self._game_engine_factory = game_engine_factory



        self.register_events()



    # Register listeners.
    def register_events(
        self
    ):
        """
        Subscribe to game events.
        """


        self._bus.subscribe(

            EventType.START_GAME,

            self.start_game

        )


        self._bus.subscribe(

            EventType.MATCH_FOUND,

            self.handle_match_found

        )


        self._bus.subscribe(

            EventType.MOVE_REQUESTED,

            self.handle_move

        )



    # Handle matched players.
    def handle_match_found(
        self,
        event
    ):
        """
        Create room for matched players.
        """

        player1 = event.data["player1"]

        player2 = event.data["player2"]


        room = self._room_manager.create_room()


        room.add_player(player1)

        room.add_player(player2)


        self._bus.publish(

            Event(

                EventType.START_GAME,

                {
                    "room_id": room.room_id
                }

            )

        )



    # Start new game.
    def start_game(
        self,
        event
    ):
        """
        Create game for room.
        """


        room_id = event.data["room_id"]



        game_id = str(
            uuid.uuid4()
        )



        game = self._game_manager.create_game(
            game_id
        )



        room = self._room_manager.get_room(
            room_id
        )


        if room:

            room.game_id = game_id



        self._bus.publish(

            Event(

                EventType.GAME_STARTED,

                {
                    "game_id": game_id,

                    "room_id": room_id

                }

            )

        )



    # Handle move request.
    def handle_move(
        self,
        event
    ):
        """
        Forward move to game manager.
        """


        game_id = event.data["game_id"]

        source = event.data["source"]

        target = event.data["target"]



        self._game_manager.handle_move(

            game_id,

            source,

            target

        )