from configReader import read_config
from trainer import init
from chat import send


def run():
    if read_config("init") == "true":
        init()
    send()


if __name__ == "__main__":
    run()