from A9Api import DType
import pdb


def debug(portname: str, script: str) -> None:
    print(portname, script)
    return
    dType = DType()
    pdb.run(script, {"dType": dType, "api": portname})