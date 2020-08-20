from DobotRPC import RPCServer, loggers
import asyncio
import platform
import os

{
    "jsonrpc": "2.0",
    "id": 1234213,
    "method": "init",
    "params": {
        "script": "cHJpbnQoMTExMSk=",
        "portname": 222
    }
}

{
    "jsonrpc": "2.0",
    "id": 1234213,
    "method": "write",
    "params": {
        "pid": 13523,
        "data": "q"
    }
}

{
    "jsonrpc": "2.0",
    "id": 1234213,
    "method": "stop",
    "params": {
        "pid": 14916
    }
}

MODUE_NAME = "Serve"


class Serve(object):
    def __init__(self, ip: str, port: int, log_name: str, log_level: str):
        super().__init__()
        self.__loop = asyncio.get_event_loop()
        self.__server = RPCServer(self.__loop, ip, port)
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

    async def __debugger_write(self, pid: int, data: str) -> None:
        temp = self.__proc_map.get(pid, None)
        if temp is None:
            raise Exception(f"Invaild pid: {pid}")
        proc = temp[0]
        data = bytes(f"{data}\n", encoding="utf8")
        proc.stdin.write(data)
        await proc.stdin.drain()

    async def __debugger_init(self, portname: str, script: str) -> None:
        debugger = "debugger.exe" if platform.system(
        ) == "windows" else "debugger"
        app_dir = os.getcwd()
        cmd = f"{app_dir}/{debugger} --portname {portname} --script {script}"

        loggers.get(MODUE_NAME).info(cmd)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        async def read_out_worker():
            try:
                while not proc.stdout.at_eof():
                    data = await proc.stdout.readline()
                    if len(data) <= 0:
                        await asyncio.sleep(0.1, loop=self.__loop)
                        continue
                    await self.__server.notify(
                        "read", {
                            "pid": proc.pid,
                            "type": "out",
                            "data": str(data, encoding="utf-8")
                        })
            except Exception as e:
                loggers.get(MODUE_NAME).warn(f"PID({proc.pid}), \
Catch exception in read out worker: {e}")
            finally:
                loggers.get(MODUE_NAME).debug(
                    f"PID({proc.pid}) read out worker exit.")

        async def read_err_worker():
            try:
                while not proc.stderr.at_eof():
                    data = await proc.stderr.readline()
                    if len(data) <= 0:
                        await asyncio.sleep(0.1, loop=self.__loop)
                        continue
                    await self.__server.notify(
                        "read", {
                            "pid": proc.pid,
                            "type": "error",
                            "data": str(data, encoding="utf-8")
                        })
            except Exception as e:
                loggers.get(MODUE_NAME).warn(f"PID({proc.pid}), \
Catch exception in read err worker: {e}")
            finally:
                loggers.get(MODUE_NAME).debug(
                    f"PID({proc.pid}) read err worker exit.")

        read_out_task = asyncio.ensure_future(read_out_worker(),
                                              loop=self.__loop)
        read_err_task = asyncio.ensure_future(read_err_worker(),
                                              loop=self.__loop)

        self.__proc_map[proc.pid] = [proc, read_out_task, read_err_task]

        return {"pid": proc.pid}

    async def __debugger_stop(self, pid: int):
        temp = self.__proc_map.get(pid, None)
        if temp is None:
            raise Exception(f"Invaild pid: {pid}")
        proc, read_out_task, read_err_task = temp
        proc.terminate()
        await asyncio.gather(proc.wait(), read_out_task, read_err_task)
        del self.__proc_map[pid]

    async def __debugger_start(self, pid: int):
        self.__debugger_write()

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
