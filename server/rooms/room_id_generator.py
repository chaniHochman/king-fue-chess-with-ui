import random
import string


class RoomIdGenerator:
    """
    Generates unique room identifiers.

    Does not store rooms.
    """


    # Create new room id.
    def generate(
        self
    ):
        """
        Return random room id.
        """

        characters = (
            string.ascii_uppercase
            +
            string.digits
        )


        return "".join(

            random.choice(characters)

            for _ in range(6)

        )