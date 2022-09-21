from ControllerBase import ControllerBase


class ClockController(ControllerBase):
    def __init__(self, brightness=0, rotate=False, show_temperature=False, flash_dot=False):
        self.brightness = brightness
        self.rotate = rotate
        self.show_temperature = show_temperature
        self.flash_dot = flash_dot

        super().__init__(22, "clock.json", "Clock")

        self.message_handlers.update({
            "light": self._set_brightness,
            "rotation": self._set_rotation,
            "temp": self._set_show_temperature,
            "flashing_dot": self._set_flashing_dot
        })

    def _set_brightness(self, characteristic: str, value: int):
        self.log_change("brightness", characteristic, value)
        self.brightness = value

    def _set_rotation(self, characteristic: str, value: bool):
        self.log_change("rotation", characteristic, value)
        self.rotate = value

    def _set_show_temperature(self, characteristic: str, value: bool):
        self.log_change("show temperature", characteristic, value)
        self.show_temperature = value

    def _set_flashing_dot(self, characteristic: str, value: bool):
        self.log_change("flashing dot", characteristic, value)
        self.flash_dot = value

