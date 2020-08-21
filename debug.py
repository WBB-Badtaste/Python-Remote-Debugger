from A9Api import DType
from DobotRPC import loggers
import asyncio
import pdb
import os
import base64

loop = asyncio.get_event_loop()


def debug(portname: str, script: str) -> None:
    loggers.set_level(loggers.DEBUG)
    loggers.set_use_console(False)
    loggers.set_use_file(True)
    loggers.set_filename(f"Debugger({os.getpid()})")

    try:
        script = base64.b64decode(script)
        dType = DType()

        pdb.run(script, {"dType": dType, "api": portname})
    except Exception as e:
        loggers.get("debugger").error(e)
