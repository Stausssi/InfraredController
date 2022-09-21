import os.path
from typing import Dict, Any, Callable, Union

from piir import Remote


class ControllerBase:
    def __init__(self, gpio: int, ir_file: str):
        self.GPIO_PIN = gpio
        self.remote = Remote(f"{os.path.dirname(__file__)}/{ir_file}", gpio)

        self.message_handlers: Dict[str, Callable[[str, Union[bool, str, int]], None]] = {}

    def handle_message(
            self,
            acc_type: str,
            characteristic: str,
            value: Union[bool, str, int],
            status: Dict[str, Union[bool, str, int]]
    ):
        self.message_handlers.get(acc_type)(characteristic, value)

    def send_ir_command(self, name: str, repeat_count=1):
        self.remote.send(name, repeat_count)
