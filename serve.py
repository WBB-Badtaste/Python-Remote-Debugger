from DobotRPC import RPCServer, loggers
from debugger import Debugger
import asyncio
import platform
import os

MODUE_NAME = "Serve"
DEBUGGER_MAX_NUM = 4


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

    def __on_debugger_die(self, pid):
        self.__proc_map.pop(pid)

    async def __debugger_create_worker(self):
        app_dir = os.getcwd()
        log_dir = self.__log_dir or app_dir
        log_level = self.__log_level
        debugger = f"{app_dir}\\debugger.exe" if platform.system(
        ) == "Windows" else f"{app_dir}/debugger"

        cmd = f"{debugger} --log_level {log_level} --log_dir {log_dir} --mode debug"

        while self.__proc_idle is None:
            try:
                debugger = Debugger(self.__loop, self.__server,
                                    self.__on_debugger_die)
                await debugger.create_process(cmd)
                self.__proc_idle = debugger
                loggers.get(MODUE_NAME).info(
                    f"Subprocess({debugger.pid}) is created.")
            except Exception as e:
                self.__proc_idle = None
                loggers.get(MODUE_NAME).exception(e)

    def __get_debugger(self, pid):
        debugger = self.__proc_map.get(pid, None)
        if debugger is None:
            raise Exception(f"Invaild pid: {pid}")
        return debugger

    async def __debugger_start(self, portname: str, script: str):
        if len(self.__proc_map) >= DEBUGGER_MAX_NUM:
            raise Exception("debugger num max")

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

    async def __quit(self):
        await self.__debugger_create_feature
        tasks = [self.__proc_idle.stop()]
        for debugger in self.__proc_map.values():
            tasks.append(debugger.stop())
        await asyncio.gather(*tasks)
        self.__loop.stop()

    def start(self) -> None:
        self.__server.register('quit', self.__quit)
        self.__server.register('start', self.__debugger_start)
        self.__server.register('pause', self.__debugger_pause)
        self.__server.register('resume', self.__debugger_resume)
        self.__server.register('stop', self.__debugger_stop)
        self.__server.register('emergency_stop',
                               self.__debugger_emergency_stop)

        try:
            loggers.get(MODUE_NAME).info("running...")
            self.__loop.run_forever()
        except Exception as e:
            loggers.get(MODUE_NAME).exception(e)
            self.__loop.close()
        finally:
            loggers.get(MODUE_NAME).info("quited.")
