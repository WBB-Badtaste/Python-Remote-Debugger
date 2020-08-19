from .serve import Serve
from .debug import debug
import click

LOG_NAME = "Dobot_Debugger_Serve"
IP = "127.0.0.1"
PORT = 9098


@click.command()
@click.option("--portname", default=None, help="Device PortName", type=str)
@click.option("--script", default=None, help="Python Script", type=str)
@click.option("--level", default="debug", help="Log Level", type=str)
def main(portname: str, script: str, level: str):
    if portname is None and script is None:
        Serve(IP, PORT, LOG_NAME, level).start()
    elif portname is not None and script is not None:
        debug(portname, script)
    else:
        raise Exception("Invaild params.")


if __name__ == "__main__":
    main()
