from DobotRPC import loggers, RPCServer
import asyncio
from functools import wraps

MODUE_NAME = "Debugger"


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        loggers.get(MODUE_NAME).debug(f"{func.__name__} invoke", *args,
                                      **kwargs)
        res = func(*args, **kwargs)
        loggers.get(MODUE_NAME).debug(f"{func.__name__} return", res)
        return res

    return with_logging


class Debugger(object):
    def __init__(self, loop, server: RPCServer):
        super().__init__()
        self.__loop = loop
        self.__server = server
        self.__proc = None
        self.__pid = None
        self.__read_out_task = None
        self.__read_err_task = None

        self.__pipe_hooks = []
        self.__state = None

    @property
    def pid(self):
        return self.__pid

    @property
    def state(self):
        return self.__state

    async def __read_err_worker(self):
        try:
            while not self.__proc.stderr.at_eof():
                data = await self.__proc.stderr.readline()
                if len(data) <= 0:
                    await asyncio.sleep(0.1, loop=self.__loop)
                    continue
                await self.__server.notify(
                    "read", {
                        "pid": self.__pid,
                        "type": "error",
                        "data": str(data, encoding="utf-8")
                    })
        except Exception as e:
            loggers.get(MODUE_NAME).warn(
                f"PID({self.__pid}), Exception in read err worker: {e}")
        finally:
            loggers.get(MODUE_NAME).debug(
                f"PID({self.__pid}) read err worker exit.")

    async def __read_out_worker(self):
        try:
            while not self.__proc.stdout.at_eof():
                out = await self.__proc.stdout.readline()
                out = str(out, encoding="utf-8")
                if len(out) <= 0:
                    await asyncio.sleep(0.1, loop=self.__loop)
                elif "PDB" in out:
                    if len(self.__pipe_hooks) > 0:
                        coro = self.__pipe_hooks.pop(0)
                        await coro()
                    else:
                        await self.__write("n")
                else:
                    await self.__server.notify("read", {
                        "pid": self.__pid,
                        "type": "out",
                        "data": out
                    })
        except Exception as e:
            loggers.get(MODUE_NAME).warn(
                f"PID({self.__pid}), Exception in read out worker: {e}")
        finally:
            loggers.get(MODUE_NAME).debug(
                f"PID({self.__pid}) read out worker exit.")

    @logit
    async def create_process(self, cmd: str) -> int:
        loggers.get(MODUE_NAME).info(cmd)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        while True:
            out, err = await asyncio.gather(proc.stdout.readline(),
                                            proc.stderr.readline())
            if len(out) > 0:
                out = str(out, encoding="utf-8")
                if "pid" in out:
                    temp = out.split(" ")
                    self.__pid = temp[1]
                    break
            elif len(err) > 0:
                e = str(err, encoding="utf-8")
                loggers.get(MODUE_NAME).error(e)
            else:
                await asyncio.sleep(0.1, loop=self.__loop)

        self.__proc = proc
        self.__read_out_task = asyncio.ensure_future(self.__read_out_worker(),
                                                     loop=self.__loop)
        self.__read_err_task = asyncio.ensure_future(self.__read_err_worker(),
                                                     loop=self.__loop)

        self.__state = "idle"

    @logit
    async def __write(self, data: str):
        data = bytes(f"{data}\n", encoding="utf8")
        self.__proc.stdin.write(data)
        await self.__proc.stdin.drain()

    @logit
    async def start(self, portname: str, script: str):
        if self.__state not in ["stop", "idle"]:
            raise Exception("Invaild state")

        await self.__write(portname)
        await self.__write(script)
        event = asyncio.Event(loop=self.__loop)

        async def __start_hook():
            await self.__write("n")
            event.set()

        self.__pipe_hooks.append(__start_hook)
        await event

        self.__state = "running"

    @logit
    async def supend(self):
        if self.__state != "running":
            raise Exception("Invaild state")

        event = asyncio.Event(loop=self.__loop)

        async def __supend_hook():
            event.set()

        self.__pipe_hooks.append(__supend_hook)
        await event

        self.__state = "supended"

    @logit
    async def resume(self):
        if self.__state != "supended":
            raise Exception("Invaild state")

        event = asyncio.Event(loop=self.__loop)

        async def __resume_hook():
            await self.__write("n")
            event.set()

        self.__pipe_hooks.append(__resume_hook)
        await event

        self.__state = "supended"

    @logit
    async def stop(self):
        if self.__state not in ["running", "idle", "supended"]:
            raise Exception("Invaild state")

        self.__proc.terminate()
        await asyncio.gather(self.__proc.wait(), self.__read_out_task,
                             self.__read_err_task)

        self.__state = "stoped"
