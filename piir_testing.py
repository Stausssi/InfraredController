from piir import Remote, decode, receive

IR_LED_PORT = 22


def remote_test():
    speakers = Remote("speakers.json", 22)
    clock = Remote("clock.json", 22)

    speakers.send("light")
    clock.send("brightness")

    while True:
        data = decode(receive(18))
        print(data)


if __name__ == '__main__':
    remote_test()
