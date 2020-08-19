from .serve import start_serve
from .debug import debug
import click


@click.command()
@click.option("--portname", default=None, help="Device PortName", type=str)
@click.option("--script", default=None, help="Python Script", type=str)
@click.option("--level", default="debug", help="Log Level", type=str)
def main(portname: str, script: str, level: str):
    if portname is None and script is None:
        start_serve(level)
    elif portname is not None and script is not None:
        debug(portname, script)
    else:
        raise Exception("Invaild params.")


if __name__ == "__main__":
    main()
