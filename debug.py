from A9Api import DType
from DobotRPC import loggers
import asyncio
import pdb
import os
import base64
import platform

loop = asyncio.get_event_loop()


def debug(log_level: str, log_dir: str) -> None:
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
    portname = input()
    script = input()

    try:
        script = base64.b64decode(script)
        dType = DType()

        pdb.run(script, {"dType": dType, "api": portname})
    except Exception as e:
        loggers.get("debugger").error(e)
