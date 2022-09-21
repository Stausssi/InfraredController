import os.path
import time
from typing import Dict, Callable, Union

from loguru import logger
from piir import Remote


class ControllerBase:
    def __init__(self, gpio: int, ir_file: str, prefix: str):
        """
        Create a new controller.

        :param gpio: The GPIO pin the IR-LED is located at
        :param ir_file: The path to the file describing the IR remote that will be simulated
        :param prefix: The prefix for logging. Ideally the name of the controller
        """

        self.GPIO_PIN = gpio
        self.remote = Remote(f"{os.path.dirname(__file__)}/{ir_file}", gpio)

        self.message_handlers: Dict[str, Callable[[str, Union[bool, str, int]], None]] = {}

        self.__prefix = prefix

    def handle_message(
            self,
            acc_type: str,
            characteristic: str,
            value: Union[bool, str, int],
            status: Dict[str, Union[bool, str, int]]
    ) -> None:
        """
        Handle the received message by selecting the desired message handler depending on the acc_type.

        :param acc_type: The accessory subtype that was modified
        :param characteristic: The characteristic of the accessory
        :param value: The new value of the characteristic
        :param status: The current status before this change
        :return: Nothing
        """

        self.message_handlers.get(acc_type)(characteristic, value)

    def send_ir_command(self, name: str, repeat_count=1, delay=1.) -> None:
        """
        Send an IR-command.

        :param name: The name of the command in the remote-config file
        :param repeat_count: The number of times this command should be sent
        :param delay: The delay (in s) between the commands
        :return: Nothing
        """

        logger.info(f"Sending the IR command '{name}' {repeat_count} times with a delay of {delay}s")

        for _ in range(repeat_count):
            self.remote.send(name)

            time.sleep(delay)

    def log_change(self, acc_type: str, characteristic: str, value) -> None:
        """
        Logs a change in the status of an accessory.

        :param acc_type: The changed accessory
        :param characteristic: The characteristic that was changed
        :param value: The new value of the characteristic
        :return: Nothing
        """

        logger.info(f"{self.__prefix} '{acc_type}' '{characteristic}' is now set to '{value}'")
