from DobotRPC import RPCServer, loggers
from A9Api import DType
import asyncio
import click
import platform
import os
import pdb

{
    "jsonrpc": "2.0",
    "id": 1234213,
    "method": "init",
    "params": {
        "code": 111111,
        "portname": 222
    }
}


def start_serve(level: str) -> None:
    APP_NAME = "Dobot_Debugger_Serve"
    IP = "127.0.0.1"
    PORT = 9098
    loop = asyncio.get_event_loop()
    server = RPCServer(loop, IP, PORT)

    def quit() -> None:
        loop.stop()

    async def debugger_init(portname: str, code: str) -> None:
        debugger = "debugger.exe" if platform.system(
        ) == "windows" else "debugger"
        app_dir = os.getcwd()
        cmd = f"{app_dir}/{debugger} --portname {portname} --code {code}"
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    loggers.set_level(loggers.DEBUG)
    loggers.set_use_console(True)
    loggers.set_use_file(False)
    loggers.set_filename(APP_NAME)
    if level == "info":
        loggers.set_level(loggers.INFO)
    elif level == "debug":
        loggers.set_level(loggers.DEBUG)
    else:
        loggers.set_level(loggers.ERROR)

    server.register('quit', quit)
    server.register('init', debugger_init)

    loggers.get(APP_NAME).info("running...")
    try:
        loop.run_forever()
    finally:
        loop.close()
    loggers.get(APP_NAME).info("quited.")


def debug(portname: str, code: str):
    print(portname, code)


@click.command()
@click.option("--portname", default=None, help="Device PortName", type=str)
@click.option("--code", default=None, help="Python Script", type=str)
@click.option("--level", default="debug", help="Log Level", type=str)
def main(portname: str, code: str, level: str):
    if portname is None and code is None:
        start_serve(level)
    elif portname is not None and code is not None:
        debug(portname, code)
    else:
        raise Exception("Invaild params.")


if __name__ == "__main__":
    main()
