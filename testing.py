import json
import time

import RPi.GPIO as GPIO
from evdev import InputDevice

IR_LED_PORT = 22


def init():
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(IR_LED_PORT, GPIO.OUT)

    with open("codes.json") as f:
        _decoder = json.JSONDecoder()
        codes = _decoder.decode(f.read())

    return codes


def listen(codes):
    ir_receiver = InputDevice("/dev/input/event0")

    active = False

    try:
        print("Listening for IR-Events...")
        for event in ir_receiver.read_loop():
            # print(categorize(event))

            # Type 4 means received signal
            if event.type == 4:
                # End if music remote is sending turn off
                if event.value == int(codes["speakers"]["power"], base=16):
                    done()

                if event.value == int(codes["speakers"]["light"], base=16):
                    active = not active
                    send(active)
                    continue

                print(f"Received keycode: {hex(event.value)}")

            time.sleep(.01)
    except KeyboardInterrupt:
        done()


def send(active):
    # GPIO.output(IR_LED_PORT, active)
    print(f"LED is now {'active' if active else 'inactive'}")
    time.sleep(.5)


def done():
    GPIO.cleanup()

    print("Done!")
    exit(0)


if __name__ == '__main__':
    listen(init())
