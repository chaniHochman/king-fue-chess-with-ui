from UI.network.tcp_client import TCPClient


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


        choice = input(
            "Choose: "
        )


        if choice == "1":

            print(
                "Searching for opponent..."
            )

            client.play()

            input(
                    "Waiting for server response..."
                )


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



        else:

            print(
                "Invalid choice"
            )



if __name__ == "__main__":

    main()