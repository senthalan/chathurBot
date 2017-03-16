from configReader import read_config
from trainer import init


def run():
    if read_config("init") == "true":
        init()


if __name__ == "__main__":
    run()