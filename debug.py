from A9Api import DType
from DobotRPC import loggers
import pdb
import os
import base64


def debug(portname: str, script: str) -> None:
    loggers.set_level(loggers.DEBUG)
    loggers.set_use_console(False)
    loggers.set_use_file(True)
    loggers.set_filename(f"debugger({os.getpid()})")

    try:

        script = base64.b64decode(script)
        dType = DType()

        pdb.run(script, {"dType": dType, "api": portname})
    except Exception as e:
        loggers.get("debugger").error(e)
