from runnable_class import Runnable


class InfraredController(Runnable):
    def __init__(self):
        print("Init")

    def __handle_message(self, message):
        print(f"Received the message: {message}")

    def send(self, message):
        super().send(message)
