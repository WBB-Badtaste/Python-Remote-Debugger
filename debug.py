from A9Api import DType
from DobotRPC import loggers
import asyncio
import pdb
import base64

loop = asyncio.get_event_loop()

MODULE_NAME = "debugger"


def debug(log_level: str, log_dir: str) -> None:
    try:
        loggers.get(MODULE_NAME).info("waitting input...")

        portname = input()
        script = input()
        script = base64.b64decode(script)
        dType = DType()

        loggers.get(MODULE_NAME).info(f"portname: {portname}")
        loggers.get(MODULE_NAME).info(f"script: {script}")

        pdb.run(script, {"dType": dType, "api": portname})
    except Exception as e:
        loggers.get(MODULE_NAME).error(e)
