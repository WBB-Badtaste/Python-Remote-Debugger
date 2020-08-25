from serve import Serve
from debug import debug
from DobotRPC import loggers
import click
import os
import platform

LOG_NAME = "Dobot_Debugger_Serve"
IP = "127.0.0.1"
PORT = 9094


@click.command()
@click.option("--mode", default=None, help="device portname", type=str)
@click.option("--log_level", default="debug", help="log level", type=str)
@click.option("--log_dir", default=None, help="log dir", type=str)
def main(mode: str, log_level: str, log_dir: str):
    if mode is None:
        loggers.set_use_console(True)
        loggers.set_use_file(False)
        loggers.set_filename(LOG_NAME)
        if log_level == "info":
            loggers.set_level(loggers.INFO)
        elif log_level == "debug":
            loggers.set_level(loggers.DEBUG)
        else:
            loggers.set_level(loggers.ERROR)

        Serve(IP, PORT, LOG_NAME, log_level, log_dir).start()
    elif mode == "debug":
        loggers.set_use_console(False)
        loggers.set_use_file(True)
        log_dir = log_dir or os.getcwd()
        log_name = f"{log_dir}\\Debugger({os.getpid()})" if platform.system(
        ) == "Windows" else f"{log_dir}/Debugger({os.getpid()})"

        loggers.set_filename(log_name)
        if log_level == "info":
            loggers.set_level(loggers.INFO)
        elif log_level == "debug":
            loggers.set_level(loggers.DEBUG)
        else:
            loggers.set_level(loggers.ERROR)

        print(f"pid {os.getpid()}")

        debug(log_level, log_dir)
    else:
        raise Exception("Invaild params.")


if __name__ == "__main__":
    main()
