from DobotRPC import RPCServer, loggers
import asyncio
import platform
import os

{
    "jsonrpc": "2.0",
    "id": 1234213,
    "method": "init",
    "params": {
        "code": 111111,
        "portname": 222
    }
}

MODUE_NAME = "Serve"


class Serve(object):
    def __init__(self, ip: str, port: int, log_name: str, log_level: str):
        super().__init__()
        self.__loop = asyncio.get_event_loop()
        self.__server = RPCServer(self.__loop, ip, port)
        loggers.set_level(loggers.DEBUG)
        loggers.set_use_console(True)
        loggers.set_use_file(False)
        loggers.set_filename(log_name)
        if log_level == "info":
            loggers.set_level(loggers.INFO)
        elif log_level == "debug":
            loggers.set_level(loggers.DEBUG)
        else:
            loggers.set_level(loggers.ERROR)

        self.__proc_map = {}
        self.__running_flag = True

    def __quit(self) -> None:
        self.__loop.stop()

    async def __debugger_write(self, pid: str, data: str) -> None:
        temp = self.__proc_map.get(pid, None)
        if temp is None:
            raise Exception(f"Invaild pid: {pid}")
        proc = temp[0]
        await proc.stdin.write(data)
        await proc.stdin.drain()

    async def __debugger_init(self, portname: str, code: str) -> None:
        debugger = "debugger.exe" if platform.system(
        ) == "windows" else "debugger"
        app_dir = os.getcwd()
        cmd = f"{app_dir}/{debugger} --portname {portname} --code {code}"
        loggers.get(MODUE_NAME).info(cmd)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        async def read_out_worker():
            while self.__running_flag:
                data = await proc.stdout.read()
                if len(data) <= 0:
                    continue
                await self.__server.notify(
                    "read", {
                        "pid": proc.pid,
                        "type": "out",
                        "data": str(data, encoding="utf-8")
                    })

        async def read_err_worker():
            while self.__running_flag:
                data = await proc.stderr.read()
                if len(data) <= 0:
                    continue
                await self.__server.notify(
                    "read", {
                        "pid": proc.pid,
                        "type": "error",
                        "data": str(data, encoding="utf-8")
                    })

        read_out_task = self.__loop.create_task(read_out_worker)
        read_err_task = self.__loop.create_task(read_err_worker)
        asyncio.get_event_loop()
        asyncio.ensure_future(read_err_task)
        asyncio.ensure_future(read_out_task)

        self.__proc_map[proc.pid] = (proc, read_out_task, read_err_task)

        return {"pid": proc.pid}

    async def __debugger_stop(self, pid: str):
        temp = self.__proc_map.get(pid, None)
        if temp is None:
            raise Exception(f"Invaild pid: {pid}")
        proc, read_out_task, read_err_task = temp
        read_out_task.cancel()
        read_err_task.cancel()
        proc.kill()

    def start(self) -> None:
        self.__server.register('quit', self.__quit)
        self.__server.register('init', self.__debugger_init)
        self.__server.register('write', self.__debugger_write)
        self.__server.register('stop', self.__debugger_stop)

        loggers.get(MODUE_NAME).info("running...")
        try:
            self.__loop.run_forever()
        finally:
            self.__loop.close()
        loggers.get(MODUE_NAME).info("quited.")
