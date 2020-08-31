from serve import Serve
from debug import debug
from DobotRPC import loggers
import click
import os
import platform

IP = "127.0.0.1"
PORT = 9099


@click.command()
@click.option("--mode", default=None, help="device portname", type=str)
@click.option("--log_level", default="debug", help="log level", type=str)
@click.option("--log_dir", default=None, help="log dir", type=str)
def main(mode: str, log_level: str, log_dir: str):
    log_dir = log_dir or os.getcwd()

    if mode is None:
        log_name = f"Debugger_Main({os.getpid()})"
        log_name = f"{log_dir}\\{log_name}" if platform.system(
        ) == "Windows" else f"{log_dir}/{log_name}"
        loggers.set_filename(log_name)
        if log_level == "info":
            loggers.set_use_console(False)
            loggers.set_use_file(True)
            loggers.set_level(loggers.INFO)
        elif log_level == "debug":
            loggers.set_use_console(True)
            loggers.set_use_file(True)
            loggers.set_level(loggers.DEBUG)
        else:
            loggers.set_use_console(False)
            loggers.set_use_file(True)
            loggers.set_level(loggers.ERROR)

        Serve(IP, PORT, log_name, log_level, log_dir).start()
    elif mode == "debug":
        loggers.set_use_console(False)
        loggers.set_use_file(True)
        log_name = f"Debugger_Sub({os.getpid()})"
        log_name = f"{log_dir}\\{log_name}" if platform.system(
        ) == "Windows" else f"{log_dir}/{log_name}"

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
