from serve import Serve
from debug import debug
import click

LOG_NAME = "Dobot_Debugger_Serve"
IP = "0.0.0.0"
PORT = 9094


@click.command()
@click.option("--mode", default=None, help="device portname", type=str)
@click.option("--level", default="debug", help="log level", type=str)
@click.option("--log_dir", default=None, help="log dir", type=str)
def main(mode: str, level: str, log_dir: str):
    if mode is None:
        Serve(IP, PORT, LOG_NAME, level, log_dir).start()
    elif mode == "debug":
        debug(level, log_dir)
    else:
        raise Exception("Invaild params.")


if __name__ == "__main__":
    main()
