import json
import sys
from threading import Thread


class InfraredController:
    def __init__(self):
        print("Init")

    def run(self):
        thread = Thread(target=self.loop)
        thread.start()

        thread.join()

    def loop(self):
        for line in sys.stdin:
            print(f"Received {line.strip()}")
            self.handle_message(json.loads(line))

    def handle_message(self, message):
        print(f"Received the message: {message}")

    def send(self, message):
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
