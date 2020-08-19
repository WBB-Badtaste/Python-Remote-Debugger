from .A9Api import DType
import pdb


def debug(portname: str, script: str):
    dType = DType()
    pdb.run(script, {"dType": dType, "api": portname})