import json
import os.path
import sys
import time
from threading import Thread
from typing import Union, Dict, Tuple, List

import requests
from loguru import logger

from ClockController import ClockController
from SpeakerController import SpeakerController


class InfraredController:
    def __init__(self):
        self.__base_url = "http://localhost:8581/api"
        acc_token = self.__authenticate()
        self.__devices = self.__get_all_devices(acc_token)

        logger.info(f"Received the devices: {self.__devices}")

        self.speaker_controller = SpeakerController(*self.__load_speaker_state())
        self.clock_controller = ClockController(*self.__load_clock_state())

        self._controllers = {
            "speaker": self.speaker_controller,
            "clock": self.clock_controller
        }

    def __authenticate(self) -> str:
        """
        Create an access token for the HomeBridge API with credentials provided by 'auth.json'.

        auth.json has to follow the format:
        ::
            {
                "username": "your_name",
                "password": "your_password"
            }

        :return: The access key
        """

        with open(f"{os.path.dirname(__file__)}/auth.json") as f:
            data = json.load(f)

        response = requests.post(f"{self.__base_url}/auth/login", data).json()
        return response["access_token"]

    def __get_all_devices(self, acc_token: str) -> List[Dict]:
        """
        Get a list of all devices that are from the speaker or clock.

        :param acc_token: The access token to use for the request.
        :return: A list of dictionaries that represent a device each
        """

        device_list = []

        while len(device_list) == 0:
            device_list = [
                device for device in requests.get(
                    f"{self.__base_url}/accessories", headers={"Authorization": f"Bearer {acc_token}"}
                ).json() if "speaker" in device["serviceName"].lower() or "clock" in device["serviceName"].lower()
            ]
            time.sleep(1)

            logger.info("No devices yet...")

        # logger.debug(
        #     requests.get(f"{self.__base_url}/accessories", headers={"Authorization": f"Bearer {acc_token}"}).json()
        # )

        return device_list

    def __load_speaker_state(self) -> Tuple[bool, bool, bool]:
        """
        Load the current state of the speaker.

        Currently supported states: power, source and light.

        :return: The states of power, source and light in that order
        """

        power, source, light = False, False, False

        for device in self.__devices:
            device_name = device["serviceName"].lower()
            if "speaker_power" in device_name:
                power = bool(device["values"]["On"])
            elif "speaker_source" in device_name:
                source = bool(device["values"]["On"])
            elif "speaker_light" in device_name:
                light = bool(device["values"]["On"])

        return power, source, light

    def __load_clock_state(self) -> Tuple[int, bool, bool, bool]:
        """
        Load the current state of the clock.

        Currently supported states: brightness, rotation, show temperature and flashing dot

        :return: The states of brightness, rotation, show temperature and flashing dot in that order
        """

        brightness, rotation, show_temp, flash_dot = 0, False, False, False

        for device in self.__devices:
            device_name = device["serviceName"].lower()
            if "clock_light" in device_name:
                brightness = int(device["values"]["Brightness"])
            elif "clock_rotation" in device_name:
                rotation = bool(device["values"]["On"])
            elif "clock_temp" in device_name:
                show_temp = bool(device["values"]["On"])
            elif "clock_flashing_dot" in device_name:
                flash_dot = bool(device["values"]["On"])

        return brightness, rotation, show_temp, flash_dot

    def run(self) -> None:
        """
        Run the loop (self.loop) in a separate thread

        :return: Nothing
        """

        thread = Thread(target=self.loop)
        thread.start()

        thread.join()

    def loop(self) -> None:
        """
        Handle every received message

        :return: Nothing
        """

        for line in sys.stdin:
            self.handle_message(json.loads(line))

    def handle_message(self, message: Dict[str, Union[bool, str, int, Dict[str, Union[bool, str, int]]]]) -> None:
        """
        Handle the received message by passing it to the corresponding controller.

        :param message: The message dictionary.
        :return: Nothing
        """

        name: str = message["name"].lower()
        target, acc_type = name.split("_", 1)

        self._controllers.get(target).handle_message(
            acc_type, message["characteristic"].lower(), message["value"], message["status"]
        )

    def send(self, message):
        logger.info(f"Writing '{message}'")
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
