from serve import Serve
from debug import debug
import click

LOG_NAME = "Dobot_Debugger_Serve"
IP = "0.0.0.0"
PORT = 9094


@click.command()
@click.option("--portname", default=None, help="device portname", type=str)
@click.option("--script", default=None, help="python script", type=str)
@click.option("--level", default="debug", help="log level", type=str)
@click.option("--log_dir", default=None, help="log dir", type=str)
def main(portname: str, script: str, level: str, log_dir: str):
    if portname is None and script is None:
        Serve(IP, PORT, LOG_NAME, level, log_dir).start()
    elif portname is not None and script is not None:
        debug(portname, script, level, log_dir)
    else:
        raise Exception("Invaild params.")


if __name__ == "__main__":
    main()
