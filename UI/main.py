from UI.network.tcp_client import TCPClient
from main import build_game
import time

def main():

    client = TCPClient()

    client.connect()


    username = input("Username: ")

    password = input("Password: ")


    client.login(
        username,
        password
    )


    while True:

        print()

        print("1. Play")
        print("2. Create Room")
        print("3. Join Room")
        print("4. Exit")
        print("5. Register")

        choice = input(
            "Choose: "
        )


        if choice == "1":

            print(
                "Searching for opponent..."
            )

            client.play()

            while True:

                message = client.get_last_message()

                print("DEBUG:", message)

                if message:

                    if message["type"] == "game_started":

                        print("STARTING GAME")

                        display = build_game()

                        print("GAME BUILT")

                        display.run()

                        break

                time.sleep(0.1)
        elif choice == "2":

            print(
                "Creating room..."
            )

            client.create_room()

            input(
                    "Waiting for room creation..."
                )


        elif choice == "3":

            room_id = input(
                "Room ID: "
            )


            print(
                "Joining room:",
                room_id
            )


            client.join_room(
                room_id
            )
            input(
                "Waiting for join result..."
            )



        elif choice == "4":

            print(
                "Closing client..."
            )

            client.disconnect()

            break

        elif choice == "5":

            username = input("Username: ")

            password = input("Password: ")

            client.register(
                username,
                password
            )

            input(
                "Waiting for registration response..."
            )


        else:

            print(
                "Invalid choice"
            )



if __name__ == "__main__":

    main()