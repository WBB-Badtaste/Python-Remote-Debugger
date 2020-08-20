from A9Api import DType
import pdb
import base64


def debug(portname: str, script: str) -> None:
    try:
        print("debug start.")
        script = base64.b64decode(script)
        print(f"debug script: {script}")
        dType = DType()
        print(f"debug 11111")
        pdb.run(script, {"dType": dType, "api": portname})
    except Exception as e:
        print(e)
