from server.server_app import ServerApp


def main():
    """
    Creates server application
    and starts the server.
    """

    app = ServerApp()

    app.start()



if __name__ == "__main__":
    main()