from DobotRPC import RPCServer, loggers
from debugger import Debugger
import asyncio
import platform
import os

{
    "jsonrpc": "2.0",
    "id": 1234213,
    "method": "start",
    "params": {
        "script": "aW1wb3J0IHRpbWUNCg0KDQp3aGlsZSAxOg0KICAgIHRpbWUuc2xlZXAoMSkNCiAgICBwcmludCgyMjIp",
        "portname": 222
    }
}

{
    "jsonrpc": "2.0",
    "id": 1234213,
    "method": "stop",
    "params": {
        "pid": 14224
    }
}

{"jsonrpc": "2.0", "id": 1234213, "method": "stop", "params": {"pid": 15254}}

{"jsonrpc": "2.0", "id": 1234213, "method": "quit", "params": {}}

MODUE_NAME = "Serve"


class Serve(object):
    def __init__(self, ip: str, port: int, log_name: str, log_level: str,
                 log_dir: str):
        super().__init__()
        self.__loop = asyncio.get_event_loop()
        self.__server = RPCServer(self.__loop, ip, port)
        self.__log_level = log_level
        self.__log_dir = log_dir
        self.__proc_map = {}
        self.__proc_idle = None
        self.__debugger_create_feature = asyncio.ensure_future(
            self.__debugger_create_worker(), loop=self.__loop)

    async def __debugger_create_worker(self):
        app_dir = os.getcwd()
        log_dir = self.__log_dir or app_dir
        log_level = self.__log_level
        debugger = f"{app_dir}\\debugger.exe" if platform.system(
        ) == "Windows" else f"{app_dir}/debugger"

        cmd = f"{debugger} --log_level {log_level} --log_dir {log_dir} --mode debug"

        debugger = Debugger(self.__loop, self.__server)

        while self.__proc_idle is None:
            try:
                debugger = Debugger(self.__loop, self.__server)
                await debugger.create_process(cmd)
                self.__proc_idle = debugger
            except Exception as e:
                loggers.get(MODUE_NAME).error(e)
                self.__proc_idle = None

    def __get_debugger(self, pid):
        debugger = self.__proc_map.get(pid, None)
        if debugger is None:
            raise Exception(f"Invaild pid: {pid}")
        return debugger

    async def __debugger_start(self, portname: str, script: str):
        await self.__debugger_create_feature
        await self.__proc_idle.start(portname, script)
        pid = self.__proc_idle.pid
        self.__proc_map[pid] = self.__proc_idle
        self.__proc_idle = None
        self.__debugger_create_feature = asyncio.ensure_future(
            self.__debugger_create_worker(), loop=self.__loop)
        return {"pid": pid}

    async def __debugger_stop(self, pid: int):
        await self.__get_debugger(pid).stop()
        del self.__proc_map[pid]

    async def __debugger_pause(self, pid: int):
        await self.__get_debugger(pid).pause()

    async def __debugger_resume(self, pid: int):
        await self.__get_debugger(pid).resume()

    async def __debugger_emergency_stop(self, pid: int):
        await self.__get_debugger(pid).emergency_stop()

    def start(self) -> None:
        self.__server.register('start', self.__debugger_start)
        self.__server.register('pause', self.__debugger_pause)
        self.__server.register('resume', self.__debugger_resume)
        self.__server.register('stop', self.__debugger_stop)
        self.__server.register('emergency_stop',
                               self.__debugger_emergency_stop)

        loggers.get(MODUE_NAME).info("running...")
        self.__loop.run_forever()
        loggers.get(MODUE_NAME).info("quited.")
