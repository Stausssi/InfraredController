import json
import sys
from threading import Thread


class Runnable:
    def run(self):
        thread = Thread(target=self.__loop)
        thread.start()

        thread.join()

    def __loop(self):
        for line in sys.stdin:
            print(f"Received {line.strip()}")
            self.__handle_message(json.loads(line))

    def __handle_message(self, message):
        raise NotImplementedError()

    def send(self, message):
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
